"""
User service for user management operations.
"""
from typing import Optional, List
from django.db import transaction
from db.repositories.user_repository import UserRepository, BlockRepository, FollowRepository
from db.repositories.message_repository import AuditLogRepository
from db.entities.user_entity import User, UserProfile, UserSettings
from common.exceptions import NotFoundError, ValidationError, ConflictError, PermissionDeniedError
from common.validators import Validator


class UserService:
    """Service for user management."""
    
    @staticmethod
    def get_user_by_id(user_id: str) -> User:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User instance
            
        Raises:
            NotFoundError: If user not found
        """
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User {user_id} not found")
        return user
    
    @staticmethod
    def get_current_user_profile(user_id: str) -> dict:
        """Get current user's full profile."""
        user = UserService.get_user_by_id(user_id)
        
        return {
            'user_id': str(user.user_id),
            'email': user.email,
            'username': user.username,
            'is_admin': user.is_admin,
            'is_banned': user.is_banned,
            'created_at': user.created_at,
            'last_login_at': user.last_login_at,
            'profile': {
                'display_name': user.profile.display_name,
                'profile_picture_url': user.profile.profile_picture_url,
                'bio': user.profile.bio,
                'location': user.profile.location,
                'privacy': user.profile.privacy,
            },
            'settings': {
                'email_notifications': user.settings.email_notifications,
                'language': user.settings.language,
            }
        }
    
    @staticmethod
    @transaction.atomic
    def update_user_profile(user_id: str, **kwargs) -> User:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update (username, display_name, bio, location, privacy, etc.)
            
        Returns:
            Updated user
        """
        user = UserService.get_user_by_id(user_id)
        
        # Update user fields
        if 'username' in kwargs:
            username = Validator.validate_username(kwargs['username'])
            # Check if username already taken
            existing = UserRepository.get_by_username(username)
            if existing and str(existing.user_id) != user_id:
                raise ConflictError("Username already taken")
            user.username = username
            user.save()
        
        # Update profile fields
        profile_fields = ['display_name', 'profile_picture_url', 'bio', 'location', 'privacy']
        profile_updated = False
        for field in profile_fields:
            if field in kwargs:
                value = kwargs[field]
                if field == 'bio':
                    value = Validator.validate_bio(value)
                setattr(user.profile, field, value)
                profile_updated = True
        
        if profile_updated:
            user.profile.save()
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='user_profile_updated',
            resource_type='user',
            resource_id=user_id
        )
        
        return user
    
    @staticmethod
    @transaction.atomic
    def update_user_settings(user_id: str, **kwargs) -> UserSettings:
        """Update user settings."""
        user = UserService.get_user_by_id(user_id)
        
        settings_fields = ['email_notifications', 'language']
        for field in settings_fields:
            if field in kwargs:
                setattr(user.settings, field, kwargs[field])
        
        user.settings.save()
        return user.settings
    
    @staticmethod
    def search_users(query: str, current_user_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[User]:
        """
        Search users by username.
        
        Args:
            query: Search query
            current_user_id: Current user ID (to exclude blocked users)
            page: Page number
            page_size: Page size
            
        Returns:
            List of users
        """
        users = UserRepository.search_by_username(query, page, page_size)
        
        # Exclude blocked users
        if current_user_id:
            users = [
                user for user in users
                if not BlockRepository.is_blocked(current_user_id, str(user.user_id))
                and not BlockRepository.is_blocked(str(user.user_id), current_user_id)
            ]
        
        return users
    
    @staticmethod
    @transaction.atomic
    def block_user(blocker_id: str, blocked_id: str, ip_address: Optional[str] = None) -> None:
        """Block a user."""
        if blocker_id == blocked_id:
            raise ValidationError("Cannot block yourself")
        
        # Check if already blocked
        if BlockRepository.is_blocked(blocker_id, blocked_id):
            raise ConflictError("User already blocked")
        
        # Create block
        BlockRepository.create(blocker_id, blocked_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=blocker_id,
            action_type='user_blocked',
            resource_type='user',
            resource_id=blocked_id,
            ip_address=ip_address
        )

    @staticmethod
    @transaction.atomic
    def unblock_user(blocker_id: str, blocked_id: str, ip_address: Optional[str] = None) -> None:
        """Unblock a user."""
        if not BlockRepository.is_blocked(blocker_id, blocked_id):
            raise NotFoundError("User not blocked")

        # Delete block
        BlockRepository.delete(blocker_id, blocked_id)

        # Audit log
        AuditLogRepository.create(
            user_id=blocker_id,
            action_type='user_unblocked',
            resource_type='user',
            resource_id=blocked_id,
            ip_address=ip_address
        )

    @staticmethod
    def get_blocked_users(user_id: str, page: int = 1, page_size: int = 20) -> List[User]:
        """Get list of blocked users."""
        return BlockRepository.get_blocked_users(user_id, page, page_size)

    @staticmethod
    def get_bulk_users(user_ids: List[str]) -> List[User]:
        """Get multiple users by IDs."""
        return UserRepository.get_bulk(user_ids)

    @staticmethod
    def can_view_profile(viewer_id: Optional[str], target_user_id: str) -> bool:
        """
        Check if viewer can view target user's profile.

        Args:
            viewer_id: Viewer user ID (None if not authenticated)
            target_user_id: Target user ID

        Returns:
            True if can view, False otherwise
        """
        target_user = UserService.get_user_by_id(target_user_id)

        # Public profiles are always visible
        if target_user.profile.privacy == 'public':
            return True

        # Not authenticated cannot view private profiles
        if not viewer_id:
            return False

        # Own profile is always visible
        if viewer_id == target_user_id:
            return True

        # Check if blocked
        if BlockRepository.is_blocked(viewer_id, target_user_id) or BlockRepository.is_blocked(target_user_id, viewer_id):
            return False

        # Private profiles require accepted follow
        follow = FollowRepository.get_follow(viewer_id, target_user_id)
        return follow is not None and follow.status == 'accepted'


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
    @transaction.atomic
    def create_user_from_firebase(firebase_uid: str, email: str, username: str, **kwargs) -> User:
        """
        Create a new user from Firebase authentication.
        
        Args:
            firebase_uid: Firebase UID from JWT
            email: User email from JWT
            username: Username (required from frontend)
            **kwargs: Additional fields:
                - profile_picture: ImageField (blob) - optional
                - bio: str - optional, default ''
                - location: str - optional, default ''
                - privacy: bool - optional, default True (public)
            
        Returns:
            Created user instance
            
        Raises:
            ConflictError: If username or email already exists
            ValidationError: If data is invalid
        """
        # Validate username
        username = Validator.validate_username(username)
        
        # Check if username already taken
        existing_username = UserRepository.get_by_username(username)
        if existing_username:
            raise ConflictError("Username already taken")
        
        # Check if email already taken
        existing_email = User.objects.filter(email=email).first()
        if existing_email:
            raise ConflictError("Email already registered")
        
        # Check if firebase_uid already exists
        existing_firebase = User.objects.filter(firebase_uid=firebase_uid).first()
        if existing_firebase:
            raise ConflictError("Firebase user already registered")
        
        # Create user
        user = User.objects.create(
            firebase_uid=firebase_uid,
            email=email,
            username=username,
            is_admin=False,
            is_banned=False
        )
        
        # Convert privacy boolean to string format for database
        privacy_bool = kwargs.get('privacy', True)  # Default: True (public)
        
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            display_name=username,  # Default display_name to username
            profile_picture=kwargs.get('profile_picture'),  # ImageField (blob)
            bio=kwargs.get('bio', ''),
            location=kwargs.get('location', ''),
            privacy=privacy_bool  # Store as boolean
        )
        
        # Create settings with defaults
        settings = UserSettings.objects.create(
            user=user,
            email_notifications=True,  # Default to True
            language='fr'  # Default to French
        )
        
        # Audit log
        AuditLogRepository.create(
            user_id=str(user.user_id),
            action_type='user_created',
            resource_type='user',
            resource_id=str(user.user_id)
        )
        
        return user
    
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
        
        # Get profile picture URL if exists
        profile_picture_url = None
        if user.profile.profile_picture:
            profile_picture_url = user.profile.profile_picture.url
        elif user.profile.profile_picture_url:  # Fallback to old URL field
            profile_picture_url = user.profile.profile_picture_url
        
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
                'profile_picture_url': profile_picture_url,
                'bio': user.profile.bio,
                'location': user.profile.location,
                'privacy': 'public' if user.profile.privacy else 'private',  # Convert boolean to string
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
                # Accept 'public'/'private' strings from API/tests and convert
                if field == 'privacy':
                    # Normalize boolean or string into the database representation
                    if isinstance(value, bool):
                        # store boolean directly
                        value = bool(value)
                    elif isinstance(value, str):
                        # accept 'public'/'private' strings from API/tests
                        value = True if value == 'public' else False
                    else:
                        value = bool(value)
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
        # Support both new and legacy field names used by tests/APIs.
        # Map legacy keys to internal model fields.
        if 'privacy_profile' in kwargs:
            user.settings.privacy_profile = kwargs.get('privacy_profile')
        if 'privacy_posts' in kwargs:
            user.settings.privacy_posts = kwargs.get('privacy_posts')

        # Notification flags
        if 'notifications_enabled' in kwargs:
            user.settings.notifications_enabled = kwargs.get('notifications_enabled')
        if 'notifications_email' in kwargs:
            user.settings.notifications_email = kwargs.get('notifications_email')

        # Backwards-compatible names
        if 'email_notifications' in kwargs:
            user.settings.email_notifications = kwargs.get('email_notifications')
        if 'language' in kwargs:
            user.settings.language = kwargs.get('language')

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

        # Check if user to block exists
        blocked_user = UserRepository.get_by_id(blocked_id)
        if not blocked_user:
            raise NotFoundError(f"User {blocked_id} not found")

        # Check if already blocked (idempotent - just return if already blocked)
        if BlockRepository.is_blocked(blocker_id, blocked_id):
            return  # Already blocked, operation is idempotent

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
        # privacy=True means public, privacy=False means private
        if target_user.profile.privacy == True:
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


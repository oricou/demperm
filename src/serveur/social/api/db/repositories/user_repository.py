"""
User repository for data access.
"""
from typing import Optional, List
from django.db.models import Q
from db.entities.user_entity import User, UserProfile, UserSettings, Block, Follow


class UserRepository:
    """Repository for User entity operations."""
    
    @staticmethod
    def get_by_id(user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            return User.objects.select_related('profile', 'settings').get(user_id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_firebase_uid(firebase_uid: str) -> Optional[User]:
        """Get user by Firebase UID."""
        try:
            return User.objects.select_related('profile', 'settings').get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get user by email."""
        try:
            return User.objects.select_related('profile', 'settings').get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        try:
            return User.objects.select_related('profile', 'settings').get(username=username)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def create(firebase_uid: str, email: str, username: str) -> User:
        """Create a new user with profile and settings."""
        user = User.objects.create(
            firebase_uid=firebase_uid,
            email=email,
            username=username
        )
        UserProfile.objects.create(user=user)
        UserSettings.objects.create(user=user)
        return user
    
    @staticmethod
    def update(user: User, **kwargs) -> User:
        """Update user fields."""
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user
    
    @staticmethod
    def search_by_username(query: str, page: int = 1, page_size: int = 20) -> List[User]:
        """Search users by username (case-insensitive)."""
        offset = (page - 1) * page_size
        return User.objects.filter(
            username__icontains=query,
            is_banned=False
        ).select_related('profile')[offset:offset + page_size]
    
    @staticmethod
    def get_bulk(user_ids: List[str]) -> List[User]:
        """Get multiple users by IDs."""
        return User.objects.filter(
            user_id__in=user_ids,
            is_banned=False
        ).select_related('profile')


class BlockRepository:
    """Repository for Block entity operations."""
    
    @staticmethod
    def create(blocker_id: str, blocked_id: str) -> Block:
        """Create a block."""
        return Block.objects.create(blocker_id=blocker_id, blocked_id=blocked_id)
    
    @staticmethod
    def delete(blocker_id: str, blocked_id: str) -> bool:
        """Delete a block."""
        deleted, _ = Block.objects.filter(blocker_id=blocker_id, blocked_id=blocked_id).delete()
        return deleted > 0
    
    @staticmethod
    def is_blocked(blocker_id: str, blocked_id: str) -> bool:
        """Check if user is blocked."""
        return Block.objects.filter(blocker_id=blocker_id, blocked_id=blocked_id).exists()
    
    @staticmethod
    def get_blocked_users(blocker_id: str, page: int = 1, page_size: int = 20) -> List[Block]:
        """Get list of blocked users."""
        offset = (page - 1) * page_size
        return Block.objects.filter(blocker_id=blocker_id).select_related('blocked')[offset:offset + page_size]


class FollowRepository:
    """Repository for Follow entity operations."""
    
    @staticmethod
    def create(follower_id: str, following_id: str, status: str = 'accepted') -> Follow:
        """Create a follow relationship."""
        return Follow.objects.create(
            follower_id=follower_id,
            following_id=following_id,
            status=status
        )
    
    @staticmethod
    def delete(follower_id: str, following_id: str) -> bool:
        """Delete a follow relationship."""
        deleted, _ = Follow.objects.filter(follower_id=follower_id, following_id=following_id).delete()
        return deleted > 0
    
    @staticmethod
    def update_status(follower_id: str, following_id: str, status: str) -> Optional[Follow]:
        """Update follow status."""
        try:
            follow = Follow.objects.get(follower_id=follower_id, following_id=following_id)
            follow.status = status
            follow.save()
            return follow
        except Follow.DoesNotExist:
            return None
    
    @staticmethod
    def get_followers(user_id: str, status: str = 'accepted', page: int = 1, page_size: int = 20) -> List[Follow]:
        """Get user's followers."""
        offset = (page - 1) * page_size
        return Follow.objects.filter(
            following_id=user_id,
            status=status
        ).select_related('follower')[offset:offset + page_size]
    
    @staticmethod
    def get_following(user_id: str, status: str = 'accepted', page: int = 1, page_size: int = 20) -> List[Follow]:
        """Get users that user is following."""
        offset = (page - 1) * page_size
        return Follow.objects.filter(
            follower_id=user_id,
            status=status
        ).select_related('following')[offset:offset + page_size]
    
    @staticmethod
    def get_pending_requests(user_id: str) -> List[Follow]:
        """Get pending follow requests for user."""
        return Follow.objects.filter(
            following_id=user_id,
            status='pending'
        ).select_related('follower')


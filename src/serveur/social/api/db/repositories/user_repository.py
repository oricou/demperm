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
    def create(email: str, username: str, firebase_uid: str = None, firebase_id: str = None) -> User:
        """Create a new user with profile and settings.

        Args:
            email: User's email address
            username: User's username
            firebase_uid: Firebase UID (preferred parameter name)
            firebase_id: Alias for firebase_uid (for backward compatibility)
        """
        # Accept both firebase_uid and firebase_id as parameter names
        uid = firebase_uid or firebase_id
        if not uid:
            raise ValueError("Either firebase_uid or firebase_id must be provided")

        user = User.objects.create(
            firebase_uid=uid,
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
    def get_blocked_users(blocker_id: str, page: int = 1, page_size: int = 20) -> List[User]:
        """Get list of blocked users (returns User objects)."""
        offset = (page - 1) * page_size
        blocks = Block.objects.filter(blocker_id=blocker_id).select_related('blocked', 'blocked__profile')[offset:offset + page_size]
        return [block.blocked for block in blocks]


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
    def get_followers(user_id: str, status: str = 'accepted', page: int = 1, page_size: int = 20) -> List[User]:
        """Get user's followers (returns User objects)."""
        offset = (page - 1) * page_size
        follows = Follow.objects.filter(
            following_id=user_id,
            status=status
        ).select_related('follower', 'follower__profile')[offset:offset + page_size]
        return [follow.follower for follow in follows]

    @staticmethod
    def get_following(user_id: str, status: str = 'accepted', page: int = 1, page_size: int = 20) -> List[User]:
        """Get users that user is following (returns User objects)."""
        offset = (page - 1) * page_size
        follows = Follow.objects.filter(
            follower_id=user_id,
            status=status
        ).select_related('following', 'following__profile')[offset:offset + page_size]
        return [follow.following for follow in follows]

    @staticmethod
    def get_follow(viewer_id:str,followed_id:str):
        follw = Follow.objects.filter(
            follower_id=viewer_id,
            following_id=followed_id
        )
        if len(follw) == 0:
            return None
        return follw[0]

    @staticmethod
    def get_pending_requests(user_id: str, page: int = 1, page_size: int = 20) -> List[Follow]:
        """Get pending follow requests for user."""
        offset = (page - 1) * page_size
        return Follow.objects.filter(
            following_id=user_id,
            status='pending'
        ).select_related('follower', 'follower__profile')[offset:offset + page_size]


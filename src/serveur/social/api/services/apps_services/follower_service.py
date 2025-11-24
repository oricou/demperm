"""
Follower service for follow/unfollow operations.
"""
from typing import List, Optional
from django.db import transaction
from db.repositories.user_repository import UserRepository, FollowRepository
from db.repositories.message_repository import AuditLogRepository
from db.entities.user_entity import Follow, User
from common.exceptions import NotFoundError, ValidationError, ConflictError, PermissionDeniedError


class FollowerService:
    """Service for follower management."""
    
    @staticmethod
    @transaction.atomic
    def follow_user(
        follower_id: str,
        followed_id: str,
        ip_address: Optional[str] = None
    ) -> Follow:
        """
        Follow a user.
        
        Args:
            follower_id: Follower user ID
            followed_id: Followed user ID
            ip_address: Client IP address
            
        Returns:
            Created follow
        """
        if follower_id == followed_id:
            raise ValidationError("Cannot follow yourself")
        
        # Check if already following
        existing_follow = FollowRepository.get_follow(follower_id, followed_id)
        if existing_follow:
            raise ConflictError("Already following or request pending")
        
        # Check if followed user exists
        followed_user = UserRepository.get_by_id(followed_id)
        if not followed_user:
            raise NotFoundError(f"User {followed_id} not found")
        
        # Determine initial status based on privacy
        if followed_user.profile.privacy == 'public':
            status = 'accepted'
        else:
            status = 'pending'
        
        # Create follow
        follow = FollowRepository.create(follower_id, followed_id, status)
        
        # Audit log
        AuditLogRepository.create(
            user_id=follower_id,
            action_type='user_followed' if status == 'accepted' else 'follow_requested',
            resource_type='user',
            resource_id=followed_id,
            ip_address=ip_address
        )
        
        return follow
    
    @staticmethod
    @transaction.atomic
    def unfollow_user(
        follower_id: str,
        followed_id: str,
        ip_address: Optional[str] = None
    ) -> None:
        """Unfollow a user."""
        follow = FollowRepository.get_follow(follower_id, followed_id)
        if not follow:
            raise NotFoundError("Not following this user")
        
        # Delete follow
        FollowRepository.delete(follower_id, followed_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=follower_id,
            action_type='user_unfollowed',
            resource_type='user',
            resource_id=followed_id,
            ip_address=ip_address
        )
    
    @staticmethod
    @transaction.atomic
    def accept_follow_request(
        followed_id: str,
        follower_id: str,
        ip_address: Optional[str] = None
    ) -> Follow:
        """Accept a follow request."""
        follow = FollowRepository.get_follow(follower_id, followed_id)
        if not follow:
            raise NotFoundError("Follow request not found")
        
        if follow.status != 'pending':
            raise ValidationError("Follow request is not pending")
        
        # Update status
        follow = FollowRepository.update_status(follower_id, followed_id, 'accepted')
        
        # Audit log
        AuditLogRepository.create(
            user_id=followed_id,
            action_type='follow_accepted',
            resource_type='user',
            resource_id=follower_id,
            ip_address=ip_address
        )
        
        return follow
    
    @staticmethod
    @transaction.atomic
    def reject_follow_request(
        followed_id: str,
        follower_id: str,
        ip_address: Optional[str] = None
    ) -> None:
        """Reject a follow request."""
        follow = FollowRepository.get_follow(follower_id, followed_id)
        if not follow:
            raise NotFoundError("Follow request not found")
        
        if follow.status != 'pending':
            raise ValidationError("Follow request is not pending")
        
        # Update status to rejected
        FollowRepository.update_status(follower_id, followed_id, 'rejected')
        
        # Audit log
        AuditLogRepository.create(
            user_id=followed_id,
            action_type='follow_rejected',
            resource_type='user',
            resource_id=follower_id,
            ip_address=ip_address
        )
    
    @staticmethod
    def get_followers(user_id: str, page: int = 1, page_size: int = 20) -> List[User]:
        """Get list of followers."""
        return FollowRepository.get_followers(user_id, page, page_size)
    
    @staticmethod
    def get_following(user_id: str, page: int = 1, page_size: int = 20) -> List[User]:
        """Get list of users being followed."""
        return FollowRepository.get_following(user_id, page, page_size)
    
    @staticmethod
    def get_pending_requests(user_id: str, page: int = 1, page_size: int = 20) -> List[Follow]:
        """Get pending follow requests."""
        return FollowRepository.get_pending_requests(user_id, page, page_size)


"""
Forum service for forum management operations.
"""
from typing import List, Optional
from django.db import transaction
from db.repositories.domain_repository import ForumRepository, SubforumRepository, MembershipRepository
from db.repositories.message_repository import AuditLogRepository
from db.entities.domain_entity import Forum, Membership
from common.exceptions import NotFoundError, ValidationError, ConflictError, PermissionDeniedError
from common.validators import Validator


class ForumService:
    """Service for forum management."""
    
    @staticmethod
    @transaction.atomic
    def create_forum(
        user_id: str,
        name: str,
        description: str,
        ip_address: Optional[str] = None
    ) -> Forum:
        """
        Create a new forum.
        
        Args:
            user_id: User ID (creator)
            name: Forum name
            description: Forum description
            ip_address: Client IP address
            
        Returns:
            Created forum
        """
        # Validate
        name = Validator.validate_forum_name(name)
        description = Validator.validate_description(description)
        
        # Create forum
        forum = ForumRepository.create(
            creator_id=user_id,
            forum_name=name,
            description=description
        )
        
        # Auto-join creator as moderator
        MembershipRepository.create(user_id, str(forum.forum_id), role='moderator')
        ForumRepository.increment_member_count(str(forum.forum_id))
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='forum_created',
            resource_type='forum',
            resource_id=str(forum.forum_id),
            ip_address=ip_address
        )
        
        return forum
    
    @staticmethod
    def get_forum_by_id(forum_id: str) -> Forum:
        """Get forum by ID."""
        forum = ForumRepository.get_by_id(forum_id)
        if not forum:
            raise NotFoundError(f"Forum {forum_id} not found")
        return forum
    
    @staticmethod
    def get_all_forums(page: int = 1, page_size: int = 20) -> List[Forum]:
        """Get all forums."""
        return ForumRepository.get_all(page, page_size)
    
    @staticmethod
    def search_forums(query: str, page: int = 1, page_size: int = 20) -> List[Forum]:
        """Search forums by name."""
        return ForumRepository.search(query, page, page_size)
    
    @staticmethod
    @transaction.atomic
    def join_forum(user_id: str, forum_id: str, ip_address: Optional[str] = None) -> Membership:
        """
        Join a forum.
        
        Args:
            user_id: User ID
            forum_id: Forum ID
            ip_address: Client IP address
            
        Returns:
            Created membership
        """
        # Check forum exists
        forum = ForumService.get_forum_by_id(forum_id)
        
        # Check if already member
        if MembershipRepository.exists(user_id, forum_id):
            raise ConflictError("Already a member of this forum")
        
        # Create membership
        membership = MembershipRepository.create(user_id, forum_id, role='member')
        
        # Increment member count
        ForumRepository.increment_member_count(forum_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='forum_joined',
            resource_type='forum',
            resource_id=forum_id,
            ip_address=ip_address
        )
        
        return membership
    
    @staticmethod
    @transaction.atomic
    def leave_forum(user_id: str, forum_id: str, ip_address: Optional[str] = None) -> None:
        """
        Leave a forum.
        
        Args:
            user_id: User ID
            forum_id: Forum ID
            ip_address: Client IP address
        """
        # Check if member
        if not MembershipRepository.exists(user_id, forum_id):
            raise NotFoundError("Not a member of this forum")
        
        # Check if creator
        forum = ForumService.get_forum_by_id(forum_id)
        if str(forum.creator_id) == user_id:
            raise PermissionDeniedError("Forum creator cannot leave the forum")
        
        # Delete membership
        MembershipRepository.delete(user_id, forum_id)
        
        # Decrement member count
        ForumRepository.decrement_member_count(forum_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='forum_left',
            resource_type='forum',
            resource_id=forum_id,
            ip_address=ip_address
        )
    
    @staticmethod
    def get_user_forums(user_id: str, page: int = 1, page_size: int = 20) -> List[Forum]:
        """Get forums user is a member of."""
        return MembershipRepository.get_user_forums(user_id, page, page_size)


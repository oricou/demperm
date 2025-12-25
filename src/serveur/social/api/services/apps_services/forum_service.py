"""
Forum service for forum management operations.
"""
from typing import List, Optional
from django.db import transaction
from django.db import IntegrityError
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
        try:
            forum = ForumRepository.create(
                creator_id=user_id,
                forum_name=name,
                description=description
            )
        except IntegrityError as exc:
            # Likely a unique constraint on forum_name - surface as a 409 Conflict
            raise ConflictError(f"Forum with name '{name}' already exists") from exc
        
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

    @staticmethod
    @transaction.atomic
    def create_subforum_in_subforum(
        user_id: str,
        parent_subforum_id: str,
        name: str,
        description: str,
        ip_address: Optional[str] = None
    ):
        """
        Create a subforum nested under another subforum.

        Args:
            user_id: User ID (creator)
            parent_subforum_id: Parent subforum ID
            name: Subforum name
            description: Subforum description
            ip_address: Client IP address

        Returns:
            Created subforum
        """
        from db.entities.domain_entity import Subforum

        # Validate
        name = Validator.validate_forum_name(name)
        description = Validator.validate_description(description)

        # Get parent subforum
        parent = SubforumRepository.get_by_id(parent_subforum_id)
        if not parent:
            raise NotFoundError(f"Parent subforum {parent_subforum_id} not found")

        # The parent subforum should have a forum_id (every subforum belongs to a forum)
        # The new subforum will have parent_forum_id = parent's forum_id
        if not parent.forum_id_id:
            raise ValidationError(f"Parent subforum {parent_subforum_id} does not have an associated forum")

        # Create the nested subforum
        subforum = SubforumRepository.create(
            creator_id=user_id,
            subforum_name=name,
            description=description,
            parent_domain_id=None,
            parent_forum_id=str(parent.forum_id_id)
        )

        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='subforum_created',
            resource_type='subforum',
            resource_id=str(subforum.subforum_id),
            details={
                'parent_subforum_id': parent_subforum_id,
                'parent_forum_id': str(parent.forum_id_id)
            },
            ip_address=ip_address
        )

        return subforum


"""
Comment service for comment management operations.
"""
from typing import Optional, List
from django.db import transaction
from db.repositories.post_repository import PostRepository, CommentRepository
from db.repositories.user_repository import UserRepository, FollowRepository
from db.repositories.message_repository import AuditLogRepository
from db.repositories.user_repository import BlockRepository
from db.entities.post_entity import Comment
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError
from common.validators import Validator


class CommentService:
    """Service for comment management."""
    
    @staticmethod
    @transaction.atomic
    def create_comment(
        user_id: str,
        post_id: str,
        content: str,
        parent_comment_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Comment:
        """
        Create a new comment.
        
        Args:
            user_id: User ID
            post_id: Post ID
            content: Comment content
            parent_comment_id: Parent comment ID (for replies)
            ip_address: Client IP address
            
        Returns:
            Created comment
        """
        # Validate
        content = Validator.validate_comment_content(content)
        
        # Check post exists
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")

        if BlockRepository.is_blocked(post.user.user_id,user_id):
            raise PermissionDeniedError("Cannot comment post from a user that blocked you")

        if post.user.profile.privacy is False:
            follow = FollowRepository.get_follow(user_id, str(post.user.user_id))
            if not follow or follow.status != 'accepted':
                raise PermissionDeniedError("Cannot view private user's post")
        # Check parent comment if provided
        if parent_comment_id:
            parent_comment = CommentRepository.get_by_id(parent_comment_id)
            if not parent_comment:
                raise NotFoundError(f"Parent comment {parent_comment_id} not found")
            if parent_comment.post.post_id != post_id:
                raise ValidationError("Parent comment does not belong to this post")
            if BlockRepository.is_blocked(parent_comment.user.user_id,user_id):
                raise PermissionDeniedError("Cannot reply to comment from a user that blocked you")

        # Create comment (repository will handle post comment count increment)
        comment = CommentRepository.create(
            user_id=user_id,
            post_id=post_id,
            content=content,
            parent_comment_id=parent_comment_id
        )
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='comment_created',
            resource_type='comment',
            resource_id=str(comment.comment_id),
            ip_address=ip_address
        )
        
        return comment
    
    @staticmethod
    def get_comment_by_id(comment_id: str) -> Comment:
        """Get comment by ID."""
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            raise NotFoundError(f"Comment {comment_id} not found")
        return comment
    
    @staticmethod
    @transaction.atomic
    def delete_comment(comment_id: str, user_id: str, ip_address: Optional[str] = None) -> None:
        """
        Delete a comment.
        
        Args:
            comment_id: Comment ID
            user_id: User ID (must be comment owner)
            ip_address: Client IP address
        """
        comment = CommentService.get_comment_by_id(comment_id)
        
        # Check permission
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User {user_id} not found")
        if comment.user.user_id != user_id and not user.is_admin:
            raise PermissionDeniedError("Not authorized to delete this comment")
        
        post_id = str(comment.post.post_id)
        nb_post_replies = len(CommentRepository.get_replies(comment_id, page=1, page_size=20))
        # Delete comment (repository will decrement post comment count for deleted rows)
        CommentRepository.delete(comment_id)
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='comment_deleted',
            resource_type='comment',
            resource_id=comment_id,
            ip_address=ip_address
        )
    
    @staticmethod
    def get_post_comments(
        post_id: str,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = 'created_at'
    ) -> List[Comment]:
        """
        Get comments for a post.
        
        Args:
            post_id: Post ID
            page: Page number
            page_size: Page size
            sort_by: Sort field (created_at or like_count)
            
        Returns:
            List of comments (top-level only, no replies)
        """
        # Check post exists
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")
        
        return CommentRepository.get_by_post(post_id, page, page_size, sort_by)
    
    @staticmethod
    def get_comment_replies(comment_id: str, page: int = 1, page_size: int = 20) -> List[Comment]:
        """Get replies to a comment."""
        # Check comment exists
        comment = CommentService.get_comment_by_id(comment_id)
        
        return CommentRepository.get_replies(comment_id, page, page_size)


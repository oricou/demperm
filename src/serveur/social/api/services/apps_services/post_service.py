"""
Post service for post management operations.
"""
from typing import Optional, List
from django.db import transaction
from db.repositories.post_repository import PostRepository, CommentRepository, LikeRepository
from db.repositories.user_repository import UserRepository, BlockRepository, FollowRepository
from db.repositories.domain_repository import SubforumRepository
from db.repositories.message_repository import AuditLogRepository
from db.entities.post_entity import Post, Comment, Like
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError, ConflictError
from common.validators import Validator
from common.utils import generate_content_signature


class PostService:
    """Service for post management."""
    
    @staticmethod
    @transaction.atomic
    def create_post(
        user_id: str,
        title: str,
        content: str,
        subforum_id: str,
        ip_address: Optional[str] = None
    ) -> Post:
        """
        Create a new post.
        
        Args:
            user_id: User ID
            title: Post title
            content: Post content
            subforum_id: Subforum ID
            ip_address: Client IP address
            
        Returns:
            Created post
        """
        # Validate
        title = Validator.validate_post_title(title)
        content = Validator.validate_post_content(content)
        
        # Check subforum exists
        subforum = SubforumRepository.get_by_id(subforum_id)
        if not subforum:
            raise NotFoundError(f"Subforum {subforum_id} not found")
        
        # Generate content signature
        signature = generate_content_signature(content)
        
        # Create post
        post = PostRepository.create(
            user_id=user_id,
            subforum_id=subforum_id,
            title=title,
            content=content,
            content_signature=signature
        )
        
        # Increment subforum post count
        SubforumRepository.increment_post_count(subforum_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='post_created',
            resource_type='post',
            resource_id=str(post.post_id),
            ip_address=ip_address
        )
        
        return post
    
    @staticmethod
    def get_post_by_id(post_id: str, viewer_id: Optional[str] = None) -> Post:
        """
        Get post by ID.
        
        Args:
            post_id: Post ID
            viewer_id: Viewer user ID (for permission check)
            
        Returns:
            Post instance
            
        Raises:
            NotFoundError: If post not found
            PermissionDeniedError: If viewer cannot view post
        """
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")
        
        # Check if viewer can view post
        if viewer_id:
            # Check if blocked
            if BlockRepository.is_blocked(viewer_id, str(post.user_id)) or \
               BlockRepository.is_blocked(str(post.user_id), viewer_id):
                raise PermissionDeniedError("Cannot view post from blocked user")
            
            # Check privacy
            if post.user.profile.privacy == 'private':
                # Check if following
                follow = FollowRepository.get_follow(viewer_id, str(post.user_id))
                if not follow or follow.status != 'accepted':
                    raise PermissionDeniedError("Cannot view private user's post")
        
        return post
    
    @staticmethod
    @transaction.atomic
    def delete_post(post_id: str, user_id: str, ip_address: Optional[str] = None) -> None:
        """
        Delete a post.
        
        Args:
            post_id: Post ID
            user_id: User ID (must be post owner or admin)
            ip_address: Client IP address
        """
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")
        
        # Check permission
        user = UserRepository.get_by_id(user_id)
        if str(post.user_id) != user_id and not user.is_admin:
            raise PermissionDeniedError("Not authorized to delete this post")
        
        # Delete post
        PostRepository.delete(post_id)
        
        # Decrement subforum post count
        SubforumRepository.decrement_post_count(str(post.subforum_id))
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='post_deleted',
            resource_type='post',
            resource_id=post_id,
            ip_address=ip_address
        )

    @staticmethod
    @transaction.atomic
    def like_post(post_id: str, user_id: str, ip_address: Optional[str] = None) -> Like:
        """Like a post."""
        post = PostService.get_post_by_id(post_id, user_id)

        # Check if already liked
        if LikeRepository.exists(user_id, post_id):
            raise ConflictError("Post already liked")

        # Create like
        like = LikeRepository.create(user_id, post_id)

        # Increment like count
        PostRepository.increment_like_count(post_id)

        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='post_liked',
            resource_type='post',
            resource_id=post_id,
            ip_address=ip_address
        )

        return like

    @staticmethod
    @transaction.atomic
    def unlike_post(post_id: str, user_id: str, ip_address: Optional[str] = None) -> None:
        """Unlike a post."""
        if not LikeRepository.exists(user_id, post_id):
            raise NotFoundError("Like not found")

        # Delete like
        LikeRepository.delete(user_id, post_id)

        # Decrement like count
        PostRepository.decrement_like_count(post_id)

        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='post_unliked',
            resource_type='post',
            resource_id=post_id,
            ip_address=ip_address
        )

    @staticmethod
    def get_post_likes(post_id: str, page: int = 1, page_size: int = 20) -> List[Like]:
        """Get users who liked a post."""
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")

        return LikeRepository.get_by_post(post_id, page, page_size)

    @staticmethod
    def get_feed(user_id: str, page: int = 1, page_size: int = 20) -> List[Post]:
        """
        Get personalized feed for user.

        Returns posts from:
        - Users the current user follows
        - Ordered by created_at DESC
        """
        return PostRepository.get_feed(user_id, page, page_size)

    @staticmethod
    def get_discover(user_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[Post]:
        """
        Get discover feed (popular posts).

        Returns:
        - Public posts
        - Ordered by popularity (likes + comments)
        - Excludes blocked users
        """
        return PostRepository.get_discover(user_id, page, page_size)


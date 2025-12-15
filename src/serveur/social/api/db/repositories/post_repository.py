"""
Post repository for data access.
"""
from typing import Optional, List
from django.db.models import F
from db.entities.post_entity import Post, Comment, Like, Tag, PostTag


class PostRepository:
    """Repository for Post entity operations."""
    
    @staticmethod
    def create(user_id: str, title: str, content: str, subforum_id: Optional[str] = None, 
               content_signature: Optional[str] = None) -> Post:
        """Create a new post."""
        return Post.objects.create(
            user_id=user_id,
            title=title,
            content=content,
            subforum_id=subforum_id,
            content_signature=content_signature
        )
    
    @staticmethod
    def get_by_id(post_id: str) -> Optional[Post]:
        """Get post by ID."""
        try:
            return Post.objects.select_related('user', 'user__profile', 'subforum').get(post_id=post_id)
        except Post.DoesNotExist:
            return None
    
    @staticmethod
    def delete(post_id: str) -> bool:
        """Delete a post."""
        deleted, _ = Post.objects.filter(post_id=post_id).delete()
        return deleted > 0
    
    @staticmethod
    def get_feed(user_id: str, page: int = 1, page_size: int = 20) -> List[Post]:
        """Get personalized feed for user."""
        # TODO: Implement logic to get posts from followed users and subscribed forums
        offset = (page - 1) * page_size
        return Post.objects.select_related('user', 'user__profile', 'subforum').order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def get_discover(page: int = 1, page_size: int = 20) -> List[Post]:
        """Get popular posts for discovery."""
        offset = (page - 1) * page_size
        return Post.objects.select_related('user', 'user__profile', 'subforum').order_by('-like_count', '-created_at')[offset:offset + page_size]
    
    @staticmethod
    def get_by_subforum(subforum_id: str, page: int = 1, page_size: int = 20) -> List[Post]:
        """Get posts in a subforum."""
        offset = (page - 1) * page_size
        return Post.objects.filter(subforum_id=subforum_id).select_related('user', 'user__profile').order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def get_by_user(user_id: str, page: int = 1, page_size: int = 20) -> List[Post]:
        """Get posts by user."""
        offset = (page - 1) * page_size
        return Post.objects.filter(user_id=user_id).select_related('subforum').order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def increment_like_count(post_id: str) -> None:
        """Increment like count."""
        Post.objects.filter(post_id=post_id).update(like_count=F('like_count') + 1)
    
    @staticmethod
    def decrement_like_count(post_id: str) -> None:
        """Decrement like count."""
        Post.objects.filter(post_id=post_id).update(like_count=F('like_count') - 1)
    
    @staticmethod
    def increment_comment_count(post_id: str) -> None:
        """Increment comment count."""
        Post.objects.filter(post_id=post_id).update(comment_count=F('comment_count') + 1)
    
    @staticmethod
    def decrement_comment_count(post_id: str) -> None:
        """Decrement comment count."""
        Post.objects.filter(post_id=post_id).update(comment_count=F('comment_count') - 1)


class CommentRepository:
    """Repository for Comment entity operations."""
    
    @staticmethod
    def create(user_id: str, post_id: str, content: str, parent_comment_id: Optional[str] = None) -> Comment:
        """Create a new comment."""
        return Comment.objects.create(
            user_id=user_id,
            post_id=post_id,
            content=content,
            parent_comment_id=parent_comment_id
        )
    
    @staticmethod
    def get_by_id(comment_id: str) -> Optional[Comment]:
        """Get comment by ID."""
        try:
            return Comment.objects.select_related('user', 'user__profile').get(comment_id=comment_id)
        except Comment.DoesNotExist:
            return None
    
    @staticmethod
    def delete(comment_id: str) -> bool:
        """Delete a comment."""
        deleted, _ = Comment.objects.filter(comment_id=comment_id).delete()
        return deleted > 0
    
    @staticmethod
    def get_by_post(post_id: str, page: int = 1, page_size: int = 20, sort_by: str = "created_at") -> List[Comment]:
        """Get comments for a post."""
        offset = (page - 1) * page_size
        return Comment.objects.filter(
            post_id=post_id,
            parent_comment_id__isnull=True
        ).select_related('user', 'user__profile').order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def get_replies(comment_id: str, page: int = 1, page_size: int = 20) -> List[Comment]:
        """Get replies to a comment."""
        offset = (page - 1) * page_size
        return Comment.objects.filter(
            parent_comment_id=comment_id
        ).select_related('user', 'user__profile').order_by('created_at')[offset:offset + page_size]


class LikeRepository:
    """Repository for Like entity operations."""
    
    @staticmethod
    def create(user_id: str, post_id: str) -> Like:
        """Create a like."""
        return Like.objects.create(user_id=user_id, post_id=post_id)
    
    @staticmethod
    def delete(user_id: str, post_id: str) -> bool:
        """Delete a like."""
        deleted, _ = Like.objects.filter(user_id=user_id, post_id=post_id).delete()
        return deleted > 0
    
    @staticmethod
    def exists(user_id: str, post_id: str) -> bool:
        """Check if like exists."""
        return Like.objects.filter(user_id=user_id, post_id=post_id).exists()
    
    @staticmethod
    def get_by_post(post_id: str, page: int = 1, page_size: int = 20) -> List[Like]:
        """Get likes for a post."""
        offset = (page - 1) * page_size
        return Like.objects.filter(post_id=post_id).select_related('user', 'user__profile').order_by('-created_at')[offset:offset + page_size]


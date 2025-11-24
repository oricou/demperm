"""
Post entity models for database layer.
"""
import uuid
from django.db import models
from django.core.validators import RegexValidator
from db.entities.user_entity import User
from db.entities.domain_entity import Subforum


class Post(models.Model):
    """User posts."""
    
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    subforum = models.ForeignKey(
        Subforum,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    title = models.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9 .,!?\'À-ÿ-]+$',
                message='Title contains invalid characters'
            )
        ]
    )
    content = models.TextField(max_length=10000)
    content_signature = models.CharField(max_length=512, null=True, blank=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['subforum']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['subforum', '-created_at']),
        ]
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comments on posts."""
    
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['parent_comment']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['post', '-created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Unknown'} on {self.post.title}"


class Like(models.Model):
    """Likes on posts."""
    
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'likes'
        unique_together = [['user', 'post']]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['post']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class Tag(models.Model):
    """Tags for categorizing posts and forums."""
    
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_-]+$',
                message='Tag name must be alphanumeric with _ or -'
            )
        ]
    )
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tags'
        indexes = [
            models.Index(fields=['tag_name']),
        ]
    
    def __str__(self):
        return self.tag_name


class PostTag(models.Model):
    """Many-to-many relationship between posts and tags."""
    
    post_tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='post_tags')
    
    class Meta:
        db_table = 'post_tags'
        unique_together = [['post', 'tag']]
    
    def __str__(self):
        return f"{self.post.title} - {self.tag.tag_name}"


class ForumTag(models.Model):
    """Many-to-many relationship between forums and tags."""
    
    forum_tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forum = models.ForeignKey('db.Forum', on_delete=models.CASCADE, related_name='forum_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='forum_tags')
    
    class Meta:
        db_table = 'forum_tags'
        unique_together = [['forum', 'tag']]
    
    def __str__(self):
        return f"{self.forum.forum_name} - {self.tag.tag_name}"


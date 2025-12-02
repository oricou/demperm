"""
Domain entity models for database layer.
"""
import uuid
from django.db import models
from django.core.validators import MinLengthValidator
from db.entities.user_entity import User


class Domain(models.Model):
    """Political domains (9 fixed domains)."""
    
    domain_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain_name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    icon_url = models.URLField(max_length=500, null=True, blank=True)
    subforum_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'domains'
        indexes = [
            models.Index(fields=['domain_name']),
        ]
    
    def __str__(self):
        return self.domain_name

    # Compatibility alias used by views/serializers in the API layer
    @property
    def name(self):
        """Alias for domain_name to keep API layer consistent."""
        return self.domain_name


class Forum(models.Model):
    """User-created forums."""
    
    forum_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_forums')
    forum_name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        validators=[MinLengthValidator(3)]
    )
    description = models.TextField(max_length=1000, null=True, blank=True)
    forum_image_url = models.URLField(max_length=500, null=True, blank=True)
    member_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'forums'
        indexes = [
            models.Index(fields=['creator']),
            models.Index(fields=['forum_name']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.forum_name

    @property
    def name(self):
        """Compatibility alias for API layer: return forum name."""
        return self.forum_name


class Subforum(models.Model):
    """Subforums (can belong to Domain or Forum)."""
    
    subforum_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # parent_id can reference either Domain or Forum (polymorphic)
    parent_domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subforums'
    )
    parent_forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subforums'
    )
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_subforums')
    subforum_name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(max_length=1000, null=True, blank=True)
    post_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subforums'
        indexes = [
            models.Index(fields=['parent_domain']),
            models.Index(fields=['parent_forum']),
            models.Index(fields=['creator']),
        ]
        constraints = [
            # Ensure exactly one parent is set
            models.CheckConstraint(
                check=(
                    models.Q(parent_domain__isnull=False, parent_forum__isnull=True) |
                    models.Q(parent_domain__isnull=True, parent_forum__isnull=False)
                ),
                name='subforum_one_parent'
            )
        ]
    
    def __str__(self):
        return self.subforum_name

    # Compatibility aliases used by views/serializers
    @property
    def name(self):
        return self.subforum_name
    


class Membership(models.Model):
    """Forum memberships."""
    
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
    ]
    
    membership_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'memberships'
        unique_together = [['user', 'forum']]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['forum']),
        ]
    
    def __str__(self):
        return f"{self.user.username} in {self.forum.forum_name}"


class SubforumSubscription(models.Model):
    """Subscriptions to subforums."""

    subscription_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subforum_subscriptions')
    subforum = models.ForeignKey(Subforum, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subforum_subscriptions'
        unique_together = [['user', 'subforum']]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['subforum']),
        ]

    def __str__(self):
        return f"{self.user.username} subscribed to {self.subforum.subforum_name}"


"""
User entity models for database layer.
"""
import uuid
from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
    """Main user table."""
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    google_id = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_-]{3,50}$',
                message='Username must be 3-50 characters, alphanumeric with _ or -'
            )
        ]
    )
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    # Minimal attributes expected when a model is used as AUTH_USER_MODEL
    # These allow Django's auth checks to pass when this model is registered
    # as the project's user model (AUTH_USER_MODEL = 'db.User').
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['google_id']),
            models.Index(fields=['username']),
        ]
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """User profile information."""
    
    PRIVACY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]
    
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, null=True, blank=True)
    profile_picture_url = models.URLField(max_length=500, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class UserSettings(models.Model):
    """User settings."""
    
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
    ]
    
    settings_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    email_notifications = models.BooleanField(default=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='fr')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_settings'
    
    def __str__(self):
        return f"Settings of {self.user.username}"


class Block(models.Model):
    """User blocks."""
    
    block_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'blocks'
        unique_together = [['blocker', 'blocked']]
        indexes = [
            models.Index(fields=['blocker']),
            models.Index(fields=['blocked']),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(blocker=models.F('blocked')),
                name='block_not_self'
            )
        ]
    
    def __str__(self):
        return f"{self.blocker.username} blocks {self.blocked.username}"


class Follow(models.Model):
    """User follows."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    follow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accepted')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'follows'
        unique_together = [['follower', 'following']]
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
            models.Index(fields=['status']),
            models.Index(fields=['follower', 'status']),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F('following')),
                name='follow_not_self'
            )
        ]
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


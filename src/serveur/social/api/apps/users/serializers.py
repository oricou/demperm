"""
Serializers for users app.
"""
from rest_framework import serializers


class UserProfileSerializer(serializers.Serializer):
    """Serializer for user profile."""
    display_name = serializers.CharField(max_length=100)
    profile_picture_url = serializers.URLField(required=False, allow_blank=True)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    location = serializers.CharField(max_length=100, required=False, allow_blank=True)
    privacy = serializers.ChoiceField(choices=['public', 'private'])


class UserSettingsSerializer(serializers.Serializer):
    """Serializer for user settings."""
    email_notifications = serializers.BooleanField()
    language = serializers.ChoiceField(choices=['fr', 'en'])


class UserSerializer(serializers.Serializer):
    """Serializer for user."""
    user_id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(max_length=30)
    is_admin = serializers.BooleanField(read_only=True)
    is_banned = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    last_login_at = serializers.DateTimeField(read_only=True)
    profile = UserProfileSerializer(read_only=True)
    settings = UserSettingsSerializer(read_only=True)


class UserPublicSerializer(serializers.Serializer):
    """Serializer for public user profile."""
    user_id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(max_length=30)
    display_name = serializers.CharField(max_length=100)
    profile_picture_url = serializers.URLField(required=False)
    bio = serializers.CharField(max_length=500, required=False)
    location = serializers.CharField(max_length=100, required=False)
    created_at = serializers.DateTimeField(read_only=True)


class UpdateUserProfileSerializer(serializers.Serializer):
    """Serializer for updating user profile."""
    username = serializers.CharField(max_length=30, required=False)
    display_name = serializers.CharField(max_length=100, required=False)
    profile_picture_url = serializers.URLField(required=False, allow_blank=True)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    location = serializers.CharField(max_length=100, required=False, allow_blank=True)
    privacy = serializers.ChoiceField(choices=['public', 'private'], required=False)


class UpdateUserSettingsSerializer(serializers.Serializer):
    """Serializer for updating user settings."""
    # Current fields
    email_notifications = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=['fr', 'en'], required=False)

    # Backwards-compatible legacy field names used by older tests/clients
    privacy_profile = serializers.BooleanField(required=False)
    privacy_posts = serializers.BooleanField(required=False)
    notifications_enabled = serializers.BooleanField(required=False)
    notifications_email = serializers.BooleanField(required=False)


class UserSearchSerializer(serializers.Serializer):
    """Serializer for user search query."""
    query = serializers.CharField(max_length=100, required=True)
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)


class UserBulkSerializer(serializers.Serializer):
    """Serializer for bulk user retrieval."""
    user_ids = serializers.ListField(
        child=serializers.UUIDField(),
        max_length=100
    )


class CreateUserSerializer(serializers.Serializer):
    """Serializer for creating a user from Firebase authentication.
    
    Firebase JWT provides: firebase_uid, email
    Frontend provides: username, profile_picture (blob), bio, location, privacy (boolean)
    """
    username = serializers.CharField(max_length=30, required=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    location = serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    privacy = serializers.BooleanField(required=False, default=True)  # True = public, False = private


"""
Serializers for followers app.
"""
from rest_framework import serializers


class FollowSerializer(serializers.Serializer):
    """Serializer for follow relationship."""
    follow_id = serializers.UUIDField(read_only=True)
    follower_id = serializers.UUIDField(read_only=True)
    following_id = serializers.UUIDField(read_only=True)
    status = serializers.ChoiceField(choices=['pending', 'accepted', 'refused'], read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class UserFollowSerializer(serializers.Serializer):
    """Serializer for user in follow context."""
    user_id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    profile_picture_url = serializers.URLField(read_only=True)


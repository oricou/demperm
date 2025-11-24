"""
Serializers for posts app.
"""
from rest_framework import serializers


class CreatePostSerializer(serializers.Serializer):
    """Serializer for creating a post."""
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=10000)
    subforum_id = serializers.UUIDField()


class PostSerializer(serializers.Serializer):
    """Serializer for post."""
    post_id = serializers.UUIDField(read_only=True)
    author_id = serializers.UUIDField(read_only=True)
    author_username = serializers.CharField(read_only=True)
    subforum_id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=10000)
    content_signature = serializers.CharField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class LikeSerializer(serializers.Serializer):
    """Serializer for like."""
    like_id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(read_only=True)
    post_id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class FeedQuerySerializer(serializers.Serializer):
    """Serializer for feed query parameters."""
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)


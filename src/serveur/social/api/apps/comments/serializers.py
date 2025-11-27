"""
Serializers for comments app.
"""
from rest_framework import serializers


class CreateCommentSerializer(serializers.Serializer):
    """Serializer for creating a comment."""
    content = serializers.CharField(max_length=2000)
    parent_comment_id = serializers.UUIDField(required=False, allow_null=True)


class CommentSerializer(serializers.Serializer):
    """Serializer for comment."""
    comment_id = serializers.UUIDField(read_only=True)
    post_id = serializers.UUIDField(read_only=True)
    author_id = serializers.UUIDField(read_only=True)
    author_username = serializers.CharField(read_only=True)
    parent_comment_id = serializers.UUIDField(read_only=True, allow_null=True)
    content = serializers.CharField(max_length=2000)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


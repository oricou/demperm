"""
Serializers for forums app.
"""
from rest_framework import serializers


class ForumSerializer(serializers.Serializer):
    """Serializer for forum."""
    forum_id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    creator_id = serializers.UUIDField(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class CreateForumSerializer(serializers.Serializer):
    """Serializer for creating a forum."""
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)


"""
Serializers for subforums app.
"""
from rest_framework import serializers


class SubforumSerializer(serializers.Serializer):
    """Serializer for subforum details."""
    subforum_id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, allow_blank=True)
    parent_domain_id = serializers.UUIDField(read_only=True, allow_null=True)
    parent_forum_id = serializers.UUIDField(read_only=True, allow_null=True)
    post_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class PostSummarySerializer(serializers.Serializer):
    """Minimal serializer for posts listed in a subforum."""
    post_id = serializers.UUIDField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=200)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

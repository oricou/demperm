"""
Serializers for tags app.
"""
from rest_framework import serializers


class TagSerializer(serializers.Serializer):
    tag_id = serializers.UUIDField(read_only=True)
    tag_name = serializers.CharField(max_length=50)
    creator_id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class CreateTagSerializer(serializers.Serializer):
    tag_name = serializers.CharField(max_length=50)


class AssignTagsSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.UUIDField(), max_length=5)

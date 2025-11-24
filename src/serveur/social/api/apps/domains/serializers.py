"""
Serializers for domains app.
"""
from rest_framework import serializers


class DomainSerializer(serializers.Serializer):
    """Serializer for domain."""
    domain_id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField(read_only=True)


class SubforumSerializer(serializers.Serializer):
    """Serializer for subforum."""
    subforum_id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    parent_domain_id = serializers.UUIDField(read_only=True, allow_null=True)
    parent_forum_id = serializers.UUIDField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)


class CreateSubforumSerializer(serializers.Serializer):
    """Serializer for creating a subforum."""
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)


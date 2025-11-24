"""
Serializers for subscriptions app.
"""
from rest_framework import serializers


class EmptyResponseSerializer(serializers.Serializer):
    """Placeholder serializer for endpoints returning no body."""
    pass

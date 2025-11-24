"""
Serializers for authentication endpoints.
"""
from rest_framework import serializers


class GoogleAuthURLSerializer(serializers.Serializer):
    """Serializer for Google auth URL request."""
    redirect_uri = serializers.URLField(required=True)


class GoogleAuthCallbackSerializer(serializers.Serializer):
    """Serializer for Google auth callback."""
    code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    redirect_uri = serializers.URLField(required=True)


class TokenRefreshSerializer(serializers.Serializer):
    """Serializer for token refresh."""
    refresh = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    """Serializer for user data in auth response."""
    user_id = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()
    is_admin = serializers.BooleanField()
    is_banned = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class AuthResponseSerializer(serializers.Serializer):
    """Serializer for authentication response."""
    user = UserSerializer()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response."""
    access_token = serializers.CharField()


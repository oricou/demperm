"""
Serializers for messages app.
"""
from rest_framework import serializers


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending a message."""
    content = serializers.CharField(max_length=5000)
    sender_public_key = serializers.CharField()
    receiver_public_key = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    """Serializer for message."""
    message_id = serializers.UUIDField(read_only=True)
    sender_id = serializers.UUIDField(read_only=True)
    receiver_id = serializers.UUIDField(read_only=True)
    encrypted_content_sender = serializers.CharField(read_only=True)
    encrypted_content_receiver = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class ConversationSerializer(serializers.Serializer):
    """Serializer for conversation summary."""
    other_user_id = serializers.UUIDField()
    other_user_username = serializers.CharField()
    last_message_at = serializers.DateTimeField()
    unread_count = serializers.IntegerField()


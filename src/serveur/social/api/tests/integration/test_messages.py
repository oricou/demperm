"""
Integration tests for Messages API.
Tests conformity with Specifications3.md section 5.10.
"""
import pytest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIClient
from db.entities.message_entity import Message
from db.entities.user_entity import User


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def user1(db):
    """Create test user 1."""
    user = User.objects.create(
        email='user1@test.com',
        username='user1',
        firebase_uid='firebase_id_1'
    )
    # Generate RSA keys for E2E encryption (simplified for tests)
    user.public_key_rsa = "-----BEGIN PUBLIC KEY-----\nMOCK_PUBLIC_KEY\n-----END PUBLIC KEY-----"
    user.save()
    # Add is_authenticated for DRF compatibility in tests
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def user2(db):
    """Create test user 2."""
    user = User.objects.create(
        email='user2@test.com',
        username='user2',
        firebase_uid='firebase_id_2'
    )
    user.public_key_rsa = "-----BEGIN PUBLIC KEY-----\nMOCK_PUBLIC_KEY\n-----END PUBLIC KEY-----"
    user.save()
    # Add is_authenticated for DRF compatibility in tests
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.mark.django_db
class TestMessagesAPI:
    """Test Messages API endpoints."""
    
    def test_get_conversations_list(self, api_client, user1, user2):
        """
        Test: GET /api/v1/messages/
        Spec: Section 5.10 - Liste les conversations de l'utilisateur
        """
        # Authenticate
        api_client.force_authenticate(user=user1)
        
        # Create a message
        Message.objects.create(
            sender=user1,
            receiver=user2,
            encrypted_content="encrypted_content_mock",
            encryption_key_sender="key_sender_mock",
            encryption_key_receiver="key_receiver_mock"
        )
        
        # Test endpoint
        response = api_client.get('/api/v1/messages/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'conversations' in response.data or isinstance(response.data, list)
    
    def test_get_conversation_with_user(self, api_client, user1, user2):
        """
        Test: GET /api/v1/messages/{user_id}/
        Spec: Section 5.10 - Messages échangés avec un utilisateur spécifique
        """
        # Authenticate
        api_client.force_authenticate(user=user1)
        
        # Create messages
        Message.objects.create(
            sender=user1,
            receiver=user2,
            encrypted_content="msg1",
            encryption_key_sender="key1",
            encryption_key_receiver="key1r"
        )
        Message.objects.create(
            sender=user2,
            receiver=user1,
            encrypted_content="msg2",
            encryption_key_sender="key2",
            encryption_key_receiver="key2r"
        )
        
        # Test endpoint
        response = api_client.get(f'/api/v1/messages/{user2.user_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list) or 'messages' in response.data
    
    @patch('services.apps_services.message_service.EncryptionService.encrypt_message')
    def test_send_message(self, mock_encrypt, api_client, user1, user2):
        """
        Test: POST /api/v1/messages/{user_id}/create/
        Spec: Section 5.10 - Envoyer un message
        """
        # Mock encryption to avoid RSA key validation
        mock_encrypt.return_value = {
            'encrypted_content': 'encrypted_mock',
            'encryption_key_sender': 'key_sender_mock',
            'encryption_key_receiver': 'key_receiver_mock'
        }
        
        # Authenticate
        api_client.force_authenticate(user=user1)
        
        # Test endpoint
        payload = {
            'content': 'Hello, this is a test message',
            'sender_public_key': user1.public_key_rsa,
            'receiver_public_key': user2.public_key_rsa
        }
        
        response = api_client.post(f'/api/v1/messages/{user2.user_id}/create/', payload, format='json')
        
        # Should create message
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]
        
        # Verify message was created
        assert Message.objects.filter(sender=user1, receiver=user2).exists()
    
    def test_send_message_to_self_forbidden(self, api_client, user1):
        """
        Test: Cannot send message to self
        Spec: Check constraint - sender_id != receiver_id
        """
        api_client.force_authenticate(user=user1)
        
        payload = {
            'content': 'Message to myself',
            'sender_public_key': user1.public_key_rsa,
            'receiver_public_key': user1.public_key_rsa
        }
        
        response = api_client.post(f'/api/v1/messages/{user1.user_id}/create/', payload, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_unauthenticated_access(self, api_client, user2):
        """
        Test: Unauthenticated users cannot access messages
        Spec: All endpoints require authentication
        """
        # No authentication
        response = api_client.get('/api/v1/messages/')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        
        response = api_client.get(f'/api/v1/messages/{user2.user_id}/')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    def test_message_encryption_fields(self, api_client, user1, user2):
        """
        Test: Message model has required E2E encryption fields
        Spec: Section 3.2 - Messages table structure
        """
        message = Message.objects.create(
            sender=user1,
            receiver=user2,
            encrypted_content="encrypted_content",
            encryption_key_sender="key_sender",
            encryption_key_receiver="key_receiver"
        )
        
        # Verify all required fields exist
        assert hasattr(message, 'message_id')
        assert hasattr(message, 'sender')
        assert hasattr(message, 'receiver')
        assert hasattr(message, 'encrypted_content')
        assert hasattr(message, 'encryption_key_sender')
        assert hasattr(message, 'encryption_key_receiver')
        assert hasattr(message, 'is_read')
        assert hasattr(message, 'created_at')
        
        # Verify defaults
        assert message.is_read == False
    
    def test_messages_marked_as_read(self, api_client, user1, user2):
        """
        Test: Messages are marked as read when fetched
        Spec: Section 5.10 - GET /messages/{user_id} marque comme lus
        """
        # Create unread message
        message = Message.objects.create(
            sender=user2,
            receiver=user1,
            encrypted_content="msg",
            encryption_key_sender="key",
            encryption_key_receiver="key_r",
            is_read=False
        )
        
        api_client.force_authenticate(user=user1)
        
        # Fetch conversation
        response = api_client.get(f'/api/v1/messages/{user2.user_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Message should be marked as read
        message.refresh_from_db()
        assert message.is_read == True
    
    def test_delete_conversation(self, api_client, user1, user2):
        """
        Test: DELETE /api/v1/messages/{user_id}/delete/
        Spec: Section 5.10 - Supprimer une conversation (soft delete)
        """
        # Create messages
        msg1 = Message.objects.create(
            sender=user1,
            receiver=user2,
            encrypted_content="msg1",
            encryption_key_sender="key1",
            encryption_key_receiver="key1r"
        )
        msg2 = Message.objects.create(
            sender=user2,
            receiver=user1,
            encrypted_content="msg2",
            encryption_key_sender="key2",
            encryption_key_receiver="key2r"
        )
        
        api_client.force_authenticate(user=user1)
        
        # Delete conversation
        response = api_client.delete(f'/api/v1/messages/{user2.user_id}/delete/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify soft delete - messages still exist but marked as deleted
        msg1.refresh_from_db()
        msg2.refresh_from_db()
        
        assert msg1.deleted_by_sender == True  # user1 sent this
        assert msg2.deleted_by_receiver == True  # user1 received this
        
        # User2 should still see their messages
        assert msg1.deleted_by_receiver == False
        assert msg2.deleted_by_sender == False
    
    def test_deleted_messages_not_shown(self, api_client, user1, user2):
        """
        Test: Deleted messages don't appear in conversation list
        Spec: Soft delete - messages hidden for user who deleted
        """
        # Create message
        Message.objects.create(
            sender=user1,
            receiver=user2,
            encrypted_content="msg",
            encryption_key_sender="key",
            encryption_key_receiver="key_r"
        )
        
        api_client.force_authenticate(user=user1)
        
        # Delete conversation
        api_client.delete(f'/api/v1/messages/{user2.user_id}/delete/')
        
        # Get conversations - should be empty for user1
        response = api_client.get('/api/v1/messages/')
        assert response.status_code == status.HTTP_200_OK
        
        conversations = response.data if isinstance(response.data, list) else response.data.get('conversations', [])
        assert len(conversations) == 0


@pytest.mark.django_db
class TestMessagesConformityWithSpecs:
    """Test conformity with Specifications3.md."""
    
    def test_routes_match_specifications(self):
        """
        Verify routes match Specifications3.md section 5.10.
        
        Expected routes:
        - GET /messages/ ✅
        - GET /messages/{user_id} ✅
        - POST /messages/{user_id}/create ✅
        - DELETE /messages/{user_id}/delete ✅
        """
        from django.urls import reverse
        from django.urls.exceptions import NoReverseMatch
        
        # These should exist
        try:
            assert reverse('messages:conversations-list')
            assert reverse('messages:conversation', kwargs={'user_id': 'test-id'})
            assert reverse('messages:send-message', kwargs={'user_id': 'test-id'})  # /create/
            assert reverse('messages:delete-conversation', kwargs={'user_id': 'test-id'})  # /delete/
        except NoReverseMatch as e:
            pytest.fail(f"Routes not properly configured: {e}")
    
    def test_message_model_matches_specs(self):
        """
        Verify Message model matches Specifications3.md section 3.2.
        
        Required fields:
        - message_id (UUID, PK) ✅
        - sender_id (FK → Users) ✅
        - receiver_id (FK → Users) ✅
        - encrypted_content (TEXT) ✅
        - encryption_key_sender (VARCHAR(512)) ✅
        - encryption_key_receiver (VARCHAR(512)) ✅
        - is_read (BOOLEAN, DEFAULT FALSE) ✅
        - created_at (TIMESTAMP) ✅
        - deleted_by_sender (BOOLEAN) ✅ (Extension - soft delete)
        - deleted_by_receiver (BOOLEAN) ✅ (Extension - soft delete)
        
        Constraints:
        - CHECK(sender_id != receiver_id) ✅
        """
        from db.entities.message_entity import Message
        
        # Verify field names
        field_names = [f.name for f in Message._meta.get_fields()]
        
        assert 'message_id' in field_names
        assert 'sender' in field_names
        assert 'receiver' in field_names
        assert 'encrypted_content' in field_names
        assert 'encryption_key_sender' in field_names
        assert 'encryption_key_receiver' in field_names
        assert 'is_read' in field_names
        assert 'created_at' in field_names
        assert 'deleted_by_sender' in field_names
        assert 'deleted_by_receiver' in field_names
        
        # Verify constraint exists
        constraints = [c.name for c in Message._meta.constraints]
        assert 'message_not_self' in constraints

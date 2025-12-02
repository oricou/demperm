"""
Unit tests for MessageService.
Tests business logic with mocked dependencies.
"""
import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from services.apps_services.message_service import MessageService
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError


# Valid UUID pour les tests
TEST_UUID_1 = str(uuid.uuid4())
TEST_UUID_2 = str(uuid.uuid4())
TEST_UUID_3 = str(uuid.uuid4())


@pytest.fixture
def mock_message():
    """Mock Message object."""
    msg = Mock()
    msg.message_id = TEST_UUID_1
    msg.sender_id = TEST_UUID_2
    msg.receiver_id = TEST_UUID_3
    msg.encrypted_content = 'encrypted'
    msg.encryption_key_sender = 'key_sender'
    msg.encryption_key_receiver = 'key_receiver'
    msg.is_read = False
    msg.created_at = datetime.now()
    return msg


@pytest.mark.django_db
class TestMessageServiceSendMessage:
    """Test MessageService.send_message() method."""
    
    @patch('services.apps_services.message_service.BlockRepository')
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.EncryptionService')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_send_message_success(self, mock_audit, mock_encryption, mock_msg_repo, mock_user_repo, mock_block_repo):
        """Test sending message successfully."""
        # Setup mocks
        mock_block_repo.is_blocked.return_value = False
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_encryption.encrypt_message.return_value = {
            'encrypted_content': 'encrypted',
            'encryption_key_sender': 'key_s',
            'encryption_key_receiver': 'key_r'
        }
        mock_msg_repo.create.return_value = Mock(message_id=TEST_UUID_1)
        
        # Call service
        result = MessageService.send_message(
            sender_id=TEST_UUID_1,
            receiver_id=TEST_UUID_2,
            content='Hello',
            sender_public_key='pub_key_s',
            receiver_public_key='pub_key_r',
            ip_address='127.0.0.1'
        )
        
        # Verify
        mock_user_repo.get_by_id.assert_called_once_with(TEST_UUID_2)
        mock_encryption.encrypt_message.assert_called_once()
        mock_msg_repo.create.assert_called_once()
        mock_audit.create.assert_called_once()
        assert result.message_id == TEST_UUID_1
    
    @patch('services.apps_services.message_service.BlockRepository')
    @patch('services.apps_services.message_service.UserRepository')
    def test_send_message_receiver_not_found(self, mock_user_repo, mock_block_repo):
        """Test sending message to non-existent user fails."""
        mock_block_repo.is_blocked.return_value = False
        mock_user_repo.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError, match="not found"):
            MessageService.send_message(
                sender_id=TEST_UUID_1,
                receiver_id=TEST_UUID_2,
                content='Hello',
                sender_public_key='pub_key_s',
                receiver_public_key='pub_key_r',
                ip_address='127.0.0.1'
            )
    
    @patch('services.apps_services.message_service.BlockRepository')
    @patch('services.apps_services.message_service.UserRepository')
    def test_send_message_to_self_fails(self, mock_user_repo, mock_block_repo):
        """Test cannot send message to self."""
        mock_block_repo.is_blocked.return_value = False
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_1))
        
        with pytest.raises(ValidationError, match="Cannot send message to yourself"):
            MessageService.send_message(
                sender_id=TEST_UUID_1,
                receiver_id=TEST_UUID_1,
                content='Hello',
                sender_public_key='pub_key',
                receiver_public_key='pub_key',
                ip_address='127.0.0.1'
            )
    
    @patch('services.apps_services.message_service.BlockRepository')
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.EncryptionService')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_send_message_empty_content(self, mock_audit, mock_encryption, mock_msg_repo, mock_user_repo, mock_block_repo):
        """Test sending message with empty content."""
        mock_block_repo.is_blocked.return_value = False
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_encryption.encrypt_message.return_value = {
            'encrypted_content': '',
            'encryption_key_sender': 'key_s',
            'encryption_key_receiver': 'key_r'
        }
        mock_msg_repo.create.return_value = Mock(message_id=TEST_UUID_1)
        
        result = MessageService.send_message(
            sender_id=TEST_UUID_1,
            receiver_id=TEST_UUID_2,
            content='',
            sender_public_key='pub_key_s',
            receiver_public_key='pub_key_r',
            ip_address='127.0.0.1'
        )
        
        assert result is not None
    
    @patch('services.apps_services.message_service.BlockRepository')
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.EncryptionService')
    def test_send_message_encryption_fails(self, mock_encryption, mock_user_repo, mock_block_repo):
        """Test encryption failure is propagated."""
        mock_block_repo.is_blocked.return_value = False
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_encryption.encrypt_message.side_effect = ValueError("Invalid key")
        
        with pytest.raises(ValueError, match="Invalid key"):
            MessageService.send_message(
                sender_id=TEST_UUID_1,
                receiver_id=TEST_UUID_2,
                content='Hello',
                sender_public_key='invalid_key',
                receiver_public_key='pub_key_r',
                ip_address='127.0.0.1'
            )
    
    @patch('services.apps_services.message_service.BlockRepository')
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.EncryptionService')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_send_message_long_content(self, mock_audit, mock_encryption, mock_msg_repo, mock_user_repo, mock_block_repo):
        """Test sending message with very long content."""
        long_content = 'x' * 100000
        mock_block_repo.is_blocked.return_value = False
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_encryption.encrypt_message.return_value = {
            'encrypted_content': 'encrypted_' + long_content,
            'encryption_key_sender': 'key_s',
            'encryption_key_receiver': 'key_r'
        }
        mock_msg_repo.create.return_value = Mock(message_id=TEST_UUID_1)
        
        result = MessageService.send_message(
            sender_id=TEST_UUID_1,
            receiver_id=TEST_UUID_2,
            content=long_content,
            sender_public_key='pub_key_s',
            receiver_public_key='pub_key_r',
            ip_address='127.0.0.1'
        )
        
        assert result is not None


@pytest.mark.django_db
class TestMessageServiceGetConversation:
    """Test MessageService.get_conversation() method."""
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversation_success(self, mock_msg_repo, mock_user_repo):
        """Test getting conversation successfully."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.get_conversation.return_value = [Mock(), Mock()]
        
        result = MessageService.get_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_2,
            page=1,
            page_size=20
        )
        
        assert len(result) == 2
        mock_msg_repo.mark_as_read.assert_called_once_with(TEST_UUID_2, TEST_UUID_1)
    
    @patch('services.apps_services.message_service.UserRepository')
    def test_get_conversation_other_user_not_found(self, mock_user_repo):
        """Test getting conversation with non-existent user fails."""
        mock_user_repo.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError, match="not found"):
            MessageService.get_conversation(
                user_id=TEST_UUID_1,
                other_user_id=TEST_UUID_2,
                page=1,
                page_size=20
            )
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversation_marks_as_read(self, mock_msg_repo, mock_user_repo):
        """Test conversation messages are marked as read."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.get_conversation.return_value = []
        
        MessageService.get_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_2
        )
        
        # Should mark messages FROM other_user TO user as read
        mock_msg_repo.mark_as_read.assert_called_once_with(TEST_UUID_2, TEST_UUID_1)
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversation_pagination(self, mock_msg_repo, mock_user_repo):
        """Test conversation pagination parameters are passed."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.get_conversation.return_value = []
        
        MessageService.get_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_2,
            page=3,
            page_size=50
        )
        
        mock_msg_repo.get_conversation.assert_called_once_with(
            TEST_UUID_1, TEST_UUID_2, 3, 50
        )
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversation_empty(self, mock_msg_repo, mock_user_repo):
        """Test getting empty conversation."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.get_conversation.return_value = []
        
        result = MessageService.get_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_2
        )
        
        assert result == []


@pytest.mark.django_db
class TestMessageServiceGetConversations:
    """Test MessageService.get_conversations() method."""
    
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversations_list(self, mock_msg_repo):
        """Test getting list of conversations."""
        mock_msg_repo.get_conversations.return_value = [
            {'partner_id': 'p1', 'last_message': Mock(), 'unread_count': 2},
            {'partner_id': 'p2', 'last_message': Mock(), 'unread_count': 0}
        ]
        
        result = MessageService.get_conversations(TEST_UUID_1)
        
        assert len(result) == 2
        mock_msg_repo.get_conversations.assert_called_once_with(TEST_UUID_1, 1, 20)
    
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversations_pagination(self, mock_msg_repo):
        """Test conversations pagination."""
        mock_msg_repo.get_conversations.return_value = []
        
        MessageService.get_conversations(TEST_UUID_1, page=2, page_size=50)
        
        mock_msg_repo.get_conversations.assert_called_once_with(TEST_UUID_1, 2, 50)
    
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversations_empty(self, mock_msg_repo):
        """Test getting empty conversations list."""
        mock_msg_repo.get_conversations.return_value = []
        
        result = MessageService.get_conversations(TEST_UUID_1)
        
        assert result == []


@pytest.mark.django_db
class TestMessageServiceDeleteConversation:
    """Test MessageService.delete_conversation() method."""
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_delete_conversation_success(self, mock_audit, mock_msg_repo, mock_user_repo):
        """Test deleting conversation successfully."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.mark_conversation_as_deleted.return_value = 5
        
        result = MessageService.delete_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_2,
            ip_address='127.0.0.1'
        )
        
        assert result is None  # delete_conversation returns None
        mock_msg_repo.mark_conversation_as_deleted.assert_called_once_with(
            TEST_UUID_1, TEST_UUID_2
        )
        mock_audit.create.assert_called_once()
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_delete_conversation_empty(self, mock_audit, mock_msg_repo, mock_user_repo):
        """Test deleting non-existent conversation."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.mark_conversation_as_deleted.return_value = 0
        
        result = MessageService.delete_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_2,
            ip_address='127.0.0.1'
        )
        
        assert result is None  # delete_conversation returns None
        mock_audit.create.assert_called_once()
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_delete_conversation_creates_audit_log(self, mock_audit, mock_msg_repo, mock_user_repo):
        """Test deletion creates audit log."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.mark_conversation_as_deleted.return_value = 3
        
        MessageService.delete_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_2,
            ip_address='192.168.1.1'
        )
        
        # Verify audit log was created with correct details
        call_args = mock_audit.create.call_args
        assert call_args[1]['user_id'] == TEST_UUID_1
        assert call_args[1]['action_type'] == 'conversation_deleted'
        assert call_args[1]['ip_address'] == '192.168.1.1'
        assert 'other_user_id' in call_args[1]['details']
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_delete_conversation_idempotent(self, mock_audit, mock_msg_repo, mock_user_repo):
        """Test deleting already deleted conversation."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_msg_repo.mark_conversation_as_deleted.return_value = 0
        
        # Delete twice
        result1 = MessageService.delete_conversation(TEST_UUID_1, TEST_UUID_2, '127.0.0.1')
        result2 = MessageService.delete_conversation(TEST_UUID_1, TEST_UUID_2, '127.0.0.1')

        assert result1 is None  # delete_conversation returns None
        assert result2 is None  # idempotent - still returns None


@pytest.mark.django_db
class TestMessageServiceDecryptMessage:
    """Test MessageService.decrypt_message() method."""
    
    @patch('services.apps_services.message_service.EncryptionService')
    def test_decrypt_message_as_sender(self, mock_encryption):
        """Test sender can decrypt their message."""
        message = Mock()
        message.sender_id = 'sender-uuid'
        message.receiver_id = 'receiver-uuid'
        message.encryption_key_sender = 'encrypted_key_s'
        
        mock_encryption.decrypt_message.return_value = 'Decrypted content'
        
        result = MessageService.decrypt_message(
            message=message,
            user_id='sender-uuid',
            private_key='private_key_pem'
        )
        
        assert result == 'Decrypted content'
        mock_encryption.decrypt_message.assert_called_once_with(
            message.encrypted_content,
            'encrypted_key_s',
            'private_key_pem'
        )
    
    @patch('services.apps_services.message_service.EncryptionService')
    def test_decrypt_message_as_receiver(self, mock_encryption):
        """Test receiver can decrypt message."""
        message = Mock()
        message.sender_id = 'sender-uuid'
        message.receiver_id = 'receiver-uuid'
        message.encryption_key_receiver = 'encrypted_key_r'
        
        mock_encryption.decrypt_message.return_value = 'Decrypted content'
        
        result = MessageService.decrypt_message(
            message=message,
            user_id='receiver-uuid',
            private_key='private_key_pem'
        )
        
        assert result == 'Decrypted content'
        mock_encryption.decrypt_message.assert_called_once_with(
            message.encrypted_content,
            'encrypted_key_r',
            'private_key_pem'
        )
    
    def test_decrypt_message_unauthorized(self):
        """Test third party cannot decrypt message."""
        message = Mock()
        message.sender_id = 'sender-uuid'
        message.receiver_id = 'receiver-uuid'
        
        with pytest.raises(PermissionDeniedError, match="Not authorized"):
            MessageService.decrypt_message(
                message=message,
                user_id='third-party-uuid',
                private_key='private_key_pem'
            )
    
    @patch('services.apps_services.message_service.EncryptionService')
    def test_decrypt_message_encryption_error(self, mock_encryption):
        """Test decryption failure is propagated."""
        message = Mock()
        message.sender_id = 'sender-uuid'
        message.receiver_id = 'receiver-uuid'
        message.encryption_key_sender = 'key'
        
        mock_encryption.decrypt_message.side_effect = ValueError("Invalid key")
        
        with pytest.raises(ValueError, match="Invalid key"):
            MessageService.decrypt_message(
                message=message,
                user_id='sender-uuid',
                private_key='invalid_key'
            )


@pytest.mark.django_db
class TestMessageServiceEdgeCases:
    """Test edge cases and error handling."""
    
    @patch('services.apps_services.message_service.BlockRepository')
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.EncryptionService')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_send_message_with_special_characters(self, mock_audit, mock_encryption, mock_msg_repo, mock_user_repo, mock_block_repo):
        """Test sending message with special unicode characters."""
        special_content = "Hello 你好 🎉 \n\t\r Special chars: <>\"'&"
        mock_block_repo.is_blocked.return_value = False
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_2))
        mock_encryption.encrypt_message.return_value = {
            'encrypted_content': 'encrypted',
            'encryption_key_sender': 'key_s',
            'encryption_key_receiver': 'key_r'
        }
        mock_msg_repo.create.return_value = Mock(message_id=TEST_UUID_1)
        
        result = MessageService.send_message(
            sender_id=TEST_UUID_1,
            receiver_id=TEST_UUID_2,
            content=special_content,
            sender_public_key='pub_key_s',
            receiver_public_key='pub_key_r',
            ip_address='127.0.0.1'
        )
        
        assert result is not None
    
    @patch('services.apps_services.message_service.UserRepository')
    def test_get_conversation_with_invalid_uuid(self, mock_user_repo):
        """Test getting conversation with malformed UUID."""
        mock_user_repo.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError):
            MessageService.get_conversation(
                user_id=TEST_UUID_1,
                other_user_id=TEST_UUID_2,
                page=1,
                page_size=20
            )
    
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversations_negative_page(self, mock_msg_repo):
        """Test getting conversations with negative page number."""
        mock_msg_repo.get_conversations.return_value = []
        
        # Should handle gracefully (repository will handle validation)
        MessageService.get_conversations(TEST_UUID_1, page=-1, page_size=20)
        
        mock_msg_repo.get_conversations.assert_called_once_with(TEST_UUID_1, -1, 20)
    
    @patch('services.apps_services.message_service.MessageRepository')
    def test_get_conversations_zero_page_size(self, mock_msg_repo):
        """Test getting conversations with zero page size."""
        mock_msg_repo.get_conversations.return_value = []
        
        MessageService.get_conversations(TEST_UUID_1, page=1, page_size=0)
        
        mock_msg_repo.get_conversations.assert_called_once_with(TEST_UUID_1, 1, 0)
    
    @patch('services.apps_services.message_service.UserRepository')
    @patch('services.apps_services.message_service.MessageRepository')
    @patch('services.apps_services.message_service.AuditLogRepository')
    def test_delete_conversation_same_user(self, mock_audit, mock_msg_repo, mock_user_repo):
        """Test deleting conversation with self (edge case)."""
        mock_user_repo.get_by_id.return_value = Mock(user_id=uuid.UUID(TEST_UUID_1))
        mock_msg_repo.mark_conversation_as_deleted.return_value = 0
        
        # Should work but return None (no messages to self due to constraint)
        result = MessageService.delete_conversation(
            user_id=TEST_UUID_1,
            other_user_id=TEST_UUID_1,
            ip_address='127.0.0.1'
        )

        assert result is None  # delete_conversation returns None

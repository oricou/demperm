"""
Unit tests for MessageRepository.
Tests all repository methods with edge cases.
"""
import pytest
from django.db import IntegrityError
from db.entities.message_entity import Message
from db.entities.user_entity import User
from db.repositories.message_repository import MessageRepository


@pytest.fixture
def users(db):
    """Create test users."""
    user1 = User.objects.create(
        email='user1@test.com',
        username='user1',
        firebase_uid='google_1'
    )
    user2 = User.objects.create(
        email='user2@test.com',
        username='user2',
        firebase_uid='google_2'
    )
    user3 = User.objects.create(
        email='user3@test.com',
        username='user3',
        firebase_uid='google_3'
    )
    return {'user1': user1, 'user2': user2, 'user3': user3}


@pytest.mark.django_db
class TestMessageRepositoryCreate:
    """Test MessageRepository.create() method."""
    
    def test_create_message_success(self, users):
        """Test creating a valid message."""
        message = MessageRepository.create(
            sender_id=str(users['user1'].user_id),
            receiver_id=str(users['user2'].user_id),
            encrypted_content='encrypted_content',
            encryption_key_sender='key_sender',
            encryption_key_receiver='key_receiver'
        )
        
        assert str(message.sender_id) == str(users['user1'].user_id)
        assert str(message.receiver_id) == str(users['user2'].user_id)
        assert message.encrypted_content == 'encrypted_content'
        assert message.encryption_key_sender == 'key_sender'
        assert message.encryption_key_receiver == 'key_receiver'
        assert message.is_read is False
        assert message.deleted_by_sender is False
        assert message.deleted_by_receiver is False
        assert message.created_at is not None
    
    def test_create_message_default_values(self, users):
        """Test message has correct default values."""
        message = MessageRepository.create(
            sender_id=str(users['user1'].user_id),
            receiver_id=str(users['user2'].user_id),
            encrypted_content='test',
            encryption_key_sender='k1',
            encryption_key_receiver='k2'
        )
        
        assert message.is_read is False
        assert message.deleted_by_sender is False
        assert message.deleted_by_receiver is False
    
    def test_create_message_to_self_fails(self, users):
        """Test cannot create message to self (constraint check)."""
        with pytest.raises(IntegrityError):
            MessageRepository.create(
                sender_id=str(users['user1'].user_id),
                receiver_id=str(users['user1'].user_id),
                encrypted_content='test',
                encryption_key_sender='k1',
                encryption_key_receiver='k2'
            )
    
    def test_create_with_empty_content(self, users):
        """Test creating message with empty encrypted content."""
        message = MessageRepository.create(
            sender_id=str(users['user1'].user_id),
            receiver_id=str(users['user2'].user_id),
            encrypted_content='',
            encryption_key_sender='k1',
            encryption_key_receiver='k2'
        )
        
        assert message.encrypted_content == ''
    
    def test_create_with_long_content(self, users):
        """Test creating message with very long encrypted content."""
        long_content = 'x' * 10000
        message = MessageRepository.create(
            sender_id=str(users['user1'].user_id),
            receiver_id=str(users['user2'].user_id),
            encrypted_content=long_content,
            encryption_key_sender='k1',
            encryption_key_receiver='k2'
        )
        
        assert len(message.encrypted_content) == 10000


@pytest.mark.django_db
class TestMessageRepositoryGetConversation:
    """Test MessageRepository.get_conversation() method."""
    
    def test_get_conversation_both_directions(self, users):
        """Test getting messages sent in both directions."""
        # Create messages in both directions
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg1',
            encryption_key_sender='k1',
            encryption_key_receiver='k1r'
        )
        Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg2',
            encryption_key_sender='k2',
            encryption_key_receiver='k2r'
        )
        
        messages = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert len(messages) == 2
    
    def test_get_conversation_excludes_deleted_by_sender(self, users):
        """Test deleted_by_sender messages are excluded for sender."""
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg1',
            encryption_key_sender='k1',
            encryption_key_receiver='k1r',
            deleted_by_sender=True
        )
        
        messages = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert len(messages) == 0
    
    def test_get_conversation_excludes_deleted_by_receiver(self, users):
        """Test deleted_by_receiver messages are excluded for receiver."""
        Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg1',
            encryption_key_sender='k1',
            encryption_key_receiver='k1r',
            deleted_by_receiver=True
        )
        
        messages = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert len(messages) == 0
    
    def test_get_conversation_shows_deleted_for_other_user(self, users):
        """Test message deleted by sender still shows for receiver."""
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg1',
            encryption_key_sender='k1',
            encryption_key_receiver='k1r',
            deleted_by_sender=True,
            deleted_by_receiver=False
        )
        
        # User2 should still see it
        messages = MessageRepository.get_conversation(
            str(users['user2'].user_id),
            str(users['user1'].user_id)
        )
        
        assert len(messages) == 1
    
    def test_get_conversation_empty(self, users):
        """Test getting conversation with no messages."""
        messages = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert len(messages) == 0
    
    def test_get_conversation_pagination(self, users):
        """Test conversation pagination."""
        # Create 25 messages
        for i in range(25):
            Message.objects.create(
                sender=users['user1'],
                receiver=users['user2'],
                encrypted_content=f'msg{i}',
                encryption_key_sender=f'k{i}',
                encryption_key_receiver=f'kr{i}'
            )
        
        # First page (20 items)
        page1 = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id),
            page=1,
            page_size=20
        )
        assert len(page1) == 20
        
        # Second page (5 items)
        page2 = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id),
            page=2,
            page_size=20
        )
        assert len(page2) == 5
    
    def test_get_conversation_order_descending(self, users):
        """Test messages are ordered by created_at DESC (newest first)."""
        msg1 = Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='oldest',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        msg2 = Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='newest',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2'
        )
        
        messages = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert messages[0].message_id == msg2.message_id
        assert messages[1].message_id == msg1.message_id
    
    def test_get_conversation_excludes_third_party(self, users):
        """Test conversation doesn't include messages from/to third parties."""
        # Message between user1 and user2
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg12',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        # Message between user1 and user3
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user3'],
            encrypted_content='msg13',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2'
        )
        
        messages = MessageRepository.get_conversation(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert len(messages) == 1
        assert messages[0].encrypted_content == 'msg12'


@pytest.mark.django_db
class TestMessageRepositoryGetConversations:
    """Test MessageRepository.get_conversations() method."""
    
    def test_get_conversations_list(self, users):
        """Test getting list of all conversations."""
        # Create conversations with user2 and user3
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg2',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        Message.objects.create(
            sender=users['user3'],
            receiver=users['user1'],
            encrypted_content='msg3',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2'
        )
        
        conversations = MessageRepository.get_conversations(str(users['user1'].user_id))
        
        assert len(conversations) == 2
    
    def test_get_conversations_has_last_message(self, users):
        """Test each conversation contains the last message."""
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='first',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        last_msg = Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='last',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2'
        )
        
        conversations = MessageRepository.get_conversations(str(users['user1'].user_id))
        
        assert len(conversations) == 1
        assert conversations[0]['last_message'].message_id == last_msg.message_id
    
    def test_get_conversations_unread_count(self, users):
        """Test unread count is accurate."""
        # 2 unread messages from user2
        Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg1',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1',
            is_read=False
        )
        Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg2',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2',
            is_read=False
        )
        # 1 read message
        Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg3',
            encryption_key_sender='k3',
            encryption_key_receiver='kr3',
            is_read=True
        )
        
        conversations = MessageRepository.get_conversations(str(users['user1'].user_id))
        
        assert len(conversations) == 1
        assert conversations[0]['unread_count'] == 2
    
    def test_get_conversations_excludes_deleted(self, users):
        """Test fully deleted conversations don't appear."""
        # Create and delete conversation
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1',
            deleted_by_sender=True
        )
        
        conversations = MessageRepository.get_conversations(str(users['user1'].user_id))
        
        assert len(conversations) == 0
    
    def test_get_conversations_sorted_by_most_recent(self, users):
        """Test conversations sorted by last message time."""
        # Old conversation with user2
        Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='old',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        # Recent conversation with user3
        Message.objects.create(
            sender=users['user3'],
            receiver=users['user1'],
            encrypted_content='recent',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2'
        )
        
        conversations = MessageRepository.get_conversations(str(users['user1'].user_id))
        
        # Most recent should be first
        assert str(conversations[0]['partner_id']) == str(users['user3'].user_id)
        assert str(conversations[1]['partner_id']) == str(users['user2'].user_id)
    
    def test_get_conversations_empty(self, users):
        """Test user with no conversations."""
        conversations = MessageRepository.get_conversations(str(users['user1'].user_id))
        
        assert len(conversations) == 0
    
    def test_get_conversations_deduplicates_partners(self, users):
        """Test multiple messages with same partner appear as single conversation."""
        # 5 messages with user2
        for i in range(5):
            Message.objects.create(
                sender=users['user1'],
                receiver=users['user2'],
                encrypted_content=f'msg{i}',
                encryption_key_sender=f'k{i}',
                encryption_key_receiver=f'kr{i}'
            )
        
        conversations = MessageRepository.get_conversations(str(users['user1'].user_id))
        
        assert len(conversations) == 1


@pytest.mark.django_db
class TestMessageRepositoryMarkAsRead:
    """Test MessageRepository.mark_as_read() method."""
    
    def test_mark_as_read_updates_messages(self, users):
        """Test marking messages as read."""
        msg1 = Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg1',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1',
            is_read=False
        )
        msg2 = Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg2',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2',
            is_read=False
        )
        
        MessageRepository.mark_as_read(
            str(users['user2'].user_id),
            str(users['user1'].user_id)
        )
        
        msg1.refresh_from_db()
        msg2.refresh_from_db()
        assert msg1.is_read is True
        assert msg2.is_read is True
    
    def test_mark_as_read_only_unread(self, users):
        """Test only unread messages are updated."""
        # Already read message
        msg_read = Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='read',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1',
            is_read=True
        )
        # Unread message
        msg_unread = Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='unread',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2',
            is_read=False
        )
        
        MessageRepository.mark_as_read(
            str(users['user2'].user_id),
            str(users['user1'].user_id)
        )
        
        msg_unread.refresh_from_db()
        assert msg_unread.is_read is True
    
    def test_mark_as_read_only_from_sender(self, users):
        """Test only messages from specific sender are marked."""
        # Message from user2
        msg_user2 = Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='from_user2',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1',
            is_read=False
        )
        # Message from user3
        msg_user3 = Message.objects.create(
            sender=users['user3'],
            receiver=users['user1'],
            encrypted_content='from_user3',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2',
            is_read=False
        )
        
        MessageRepository.mark_as_read(
            str(users['user2'].user_id),
            str(users['user1'].user_id)
        )
        
        msg_user2.refresh_from_db()
        msg_user3.refresh_from_db()
        assert msg_user2.is_read is True
        assert msg_user3.is_read is False
    
    def test_mark_as_read_no_messages(self, users):
        """Test mark_as_read with no messages doesn't fail."""
        # Should not raise any exception
        MessageRepository.mark_as_read(
            str(users['user2'].user_id),
            str(users['user1'].user_id)
        )


@pytest.mark.django_db
class TestMessageRepositoryMarkConversationAsDeleted:
    """Test MessageRepository.mark_conversation_as_deleted() method."""
    
    def test_mark_deleted_sender_side(self, users):
        """Test marking conversation as deleted from sender side."""
        msg = Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        
        count = MessageRepository.mark_conversation_as_deleted(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        msg.refresh_from_db()
        assert msg.deleted_by_sender is True
        assert msg.deleted_by_receiver is False
        assert count == 1
    
    def test_mark_deleted_receiver_side(self, users):
        """Test marking conversation as deleted from receiver side."""
        msg = Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        
        count = MessageRepository.mark_conversation_as_deleted(
            str(users['user2'].user_id),
            str(users['user1'].user_id)
        )
        
        msg.refresh_from_db()
        assert msg.deleted_by_sender is False
        assert msg.deleted_by_receiver is True
        assert count == 1
    
    def test_mark_deleted_both_directions(self, users):
        """Test deleting messages in both directions."""
        # Message from user1 to user2
        msg1 = Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg1',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        # Message from user2 to user1
        msg2 = Message.objects.create(
            sender=users['user2'],
            receiver=users['user1'],
            encrypted_content='msg2',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2'
        )
        
        count = MessageRepository.mark_conversation_as_deleted(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        msg1.refresh_from_db()
        msg2.refresh_from_db()
        assert msg1.deleted_by_sender is True
        assert msg2.deleted_by_receiver is True
        assert count == 2
    
    def test_mark_deleted_idempotent(self, users):
        """Test marking already deleted conversation doesn't fail."""
        msg = Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1',
            deleted_by_sender=True
        )
        
        # Delete again - should return 0 since already deleted
        count = MessageRepository.mark_conversation_as_deleted(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        msg.refresh_from_db()
        assert msg.deleted_by_sender is True
        assert count == 0  # No messages updated since already deleted
    
    def test_mark_deleted_returns_count(self, users):
        """Test returns number of messages marked as deleted."""
        # Create 5 messages
        for i in range(5):
            Message.objects.create(
                sender=users['user1'],
                receiver=users['user2'],
                encrypted_content=f'msg{i}',
                encryption_key_sender=f'k{i}',
                encryption_key_receiver=f'kr{i}'
            )
        
        count = MessageRepository.mark_conversation_as_deleted(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert count == 5
    
    def test_mark_deleted_no_messages(self, users):
        """Test deleting non-existent conversation."""
        count = MessageRepository.mark_conversation_as_deleted(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        assert count == 0
    
    def test_mark_deleted_doesnt_affect_other_conversations(self, users):
        """Test deleting conversation doesn't affect other conversations."""
        # Conversation with user2
        msg_user2 = Message.objects.create(
            sender=users['user1'],
            receiver=users['user2'],
            encrypted_content='msg2',
            encryption_key_sender='k1',
            encryption_key_receiver='kr1'
        )
        # Conversation with user3
        msg_user3 = Message.objects.create(
            sender=users['user1'],
            receiver=users['user3'],
            encrypted_content='msg3',
            encryption_key_sender='k2',
            encryption_key_receiver='kr2'
        )
        
        MessageRepository.mark_conversation_as_deleted(
            str(users['user1'].user_id),
            str(users['user2'].user_id)
        )
        
        msg_user2.refresh_from_db()
        msg_user3.refresh_from_db()
        assert msg_user2.deleted_by_sender is True
        assert msg_user3.deleted_by_sender is False

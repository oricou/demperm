"""
Message service for E2E encrypted messaging.
"""
from typing import List, Optional, Dict
from django.db import transaction
from db.repositories.message_repository import MessageRepository, AuditLogRepository
from db.repositories.user_repository import UserRepository, BlockRepository
from db.entities.message_entity import Message
from services.apps_services.encryption_service import EncryptionService
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError


class MessageService:
    """Service for E2E encrypted messaging."""
    
    @staticmethod
    @transaction.atomic
    def send_message(
        sender_id: str,
        receiver_id: str,
        content: str,
        sender_public_key: str,
        receiver_public_key: str,
        ip_address: Optional[str] = None
    ) -> Message:
        """
        Send an E2E encrypted message.
        
        Args:
            sender_id: Sender user ID
            receiver_id: Receiver user ID
            content: Plain text message content
            sender_public_key: Sender's RSA public key (PEM format)
            receiver_public_key: Receiver's RSA public key (PEM format)
            ip_address: Client IP address
            
        Returns:
            Created message
        """
        if sender_id == receiver_id:
            raise ValidationError("Cannot send message to yourself")
        
        # Check if receiver exists
        receiver = UserRepository.get_by_id(receiver_id)
        if not receiver:
            raise NotFoundError(f"User {receiver_id} not found")
        
        # Check if blocked
        if BlockRepository.is_blocked(sender_id, receiver_id) or \
           BlockRepository.is_blocked(receiver_id, sender_id):
            raise PermissionDeniedError("Cannot send message to blocked user")
        
        # Encrypt message for both sender and receiver
        encrypted_data = EncryptionService.encrypt_message(
            content,
            sender_public_key,
            receiver_public_key
        )
        
        # Create message
        message = MessageRepository.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            encrypted_content=encrypted_data['encrypted_content'],
            encryption_key_sender=encrypted_data['encryption_key_sender'],
            encryption_key_receiver=encrypted_data['encryption_key_receiver']
        )
        
        # Audit log
        AuditLogRepository.create(
            user_id=sender_id,
            action_type='message_sent',
            resource_type='message',
            resource_id=str(message.message_id),
            details={'receiver_id': receiver_id},
            ip_address=ip_address
        )
        
        return message
    
    @staticmethod
    def decrypt_message(message: Message, user_id: str, private_key: str) -> str:
        """
        Decrypt a message.
        
        Args:
            message: Message instance
            user_id: User ID (must be sender or receiver)
            private_key: User's RSA private key (PEM format)
            
        Returns:
            Decrypted message content
        """
        # Check permission
        if str(message.sender_id) != user_id and str(message.receiver_id) != user_id:
            raise PermissionDeniedError("Not authorized to decrypt this message")
        
        # Get appropriate encryption key
        if str(message.sender_id) == user_id:
            encryption_key = message.encryption_key_sender
        else:
            encryption_key = message.encryption_key_receiver
        
        # Decrypt
        decrypted_content = EncryptionService.decrypt_message(
            message.encrypted_content,
            encryption_key,
            private_key
        )
        
        return decrypted_content
    
    @staticmethod
    def get_conversation(
        user_id: str,
        other_user_id: str,
        page: int = 1,
        page_size: int = 50
    ) -> List[Message]:
        """
        Get conversation between two users.
        
        Args:
            user_id: Current user ID
            other_user_id: Other user ID
            page: Page number
            page_size: Page size
            
        Returns:
            List of messages
        """
        # Check if other user exists
        other_user = UserRepository.get_by_id(other_user_id)
        if not other_user:
            raise NotFoundError(f"User {other_user_id} not found")
        
        # Get conversation
        messages = MessageRepository.get_conversation(user_id, other_user_id, page, page_size)
        
        # Mark messages as read (messages sent by other_user TO user_id)
        MessageRepository.mark_as_read(other_user_id, user_id)
        
        return messages
    
    @staticmethod
    def get_conversations(user_id: str, page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        Get list of conversations for a user.
        
        Args:
            user_id: User ID
            page: Page number
            page_size: Page size
            
        Returns:
            List of conversations with last message
        """
        return MessageRepository.get_conversations(user_id, page, page_size)
    
    @staticmethod
    @transaction.atomic
    def delete_conversation(
        user_id: str,
        other_user_id: str,
        ip_address: Optional[str] = None
    ) -> None:
        """
        Delete a conversation (soft delete - only for current user).
        Messages are marked as deleted for the user but preserved for the other user.
        
        Args:
            user_id: Current user ID
            other_user_id: Other user ID
            ip_address: Client IP address for audit
        """
        # Check if other user exists
        other_user = UserRepository.get_by_id(other_user_id)
        if not other_user:
            raise NotFoundError(f"User {other_user_id} not found")
        
        # Mark all messages as deleted for current user
        MessageRepository.mark_conversation_as_deleted(user_id, other_user_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=user_id,
            action_type='conversation_deleted',
            resource_type='message',
            resource_id=None,
            details={'other_user_id': other_user_id},
            ip_address=ip_address
        )


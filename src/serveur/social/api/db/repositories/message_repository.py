"""
Message and Report repository for data access.
"""
from typing import Optional, List
from django.db.models import Q
from db.entities.message_entity import Message, Report, AuditLog


class MessageRepository:
    """Repository for Message entity operations."""
    
    @staticmethod
    def create(sender_id: str, receiver_id: str, encrypted_content: str,
               encryption_key_sender: str, encryption_key_receiver: str) -> Message:
        """Create a new message."""
        return Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            encrypted_content=encrypted_content,
            encryption_key_sender=encryption_key_sender,
            encryption_key_receiver=encryption_key_receiver
        )
    
    @staticmethod
    def get_conversation(user1_id: str, user2_id: str, page: int = 1, page_size: int = 20) -> List[Message]:
        """Get messages between two users."""
        offset = (page - 1) * page_size
        return Message.objects.filter(
            Q(sender_id=user1_id, receiver_id=user2_id) |
            Q(sender_id=user2_id, receiver_id=user1_id)
        ).select_related('sender', 'receiver').order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def get_conversations(user_id: str) -> List[dict]:
        """Get list of conversations for user."""
        # Get unique conversation partners
        sent = Message.objects.filter(sender_id=user_id).values_list('receiver_id', flat=True).distinct()
        received = Message.objects.filter(receiver_id=user_id).values_list('sender_id', flat=True).distinct()
        partner_ids = set(list(sent) + list(received))
        
        conversations = []
        for partner_id in partner_ids:
            last_message = Message.objects.filter(
                Q(sender_id=user_id, receiver_id=partner_id) |
                Q(sender_id=partner_id, receiver_id=user_id)
            ).select_related('sender', 'receiver').order_by('-created_at').first()
            
            unread_count = Message.objects.filter(
                sender_id=partner_id,
                receiver_id=user_id,
                is_read=False
            ).count()
            
            conversations.append({
                'partner_id': partner_id,
                'last_message': last_message,
                'unread_count': unread_count
            })
        
        return sorted(conversations, key=lambda x: x['last_message'].created_at, reverse=True)
    
    @staticmethod
    def mark_as_read(sender_id: str, receiver_id: str) -> None:
        """Mark messages as read."""
        Message.objects.filter(sender_id=sender_id, receiver_id=receiver_id, is_read=False).update(is_read=True)


class ReportRepository:
    """Repository for Report entity operations."""
    
    @staticmethod
    def create(reporter_id: str, target_type: str, target_id: str, reason: str, 
               description: Optional[str] = None) -> Report:
        """Create a new report."""
        return Report.objects.create(
            reporter_id=reporter_id,
            target_type=target_type,
            target_id=target_id,
            reason=reason,
            description=description
        )
    
    @staticmethod
    def get_by_id(report_id: str) -> Optional[Report]:
        """Get report by ID."""
        try:
            return Report.objects.select_related('reporter', 'resolved_by').get(report_id=report_id)
        except Report.DoesNotExist:
            return None
    
    @staticmethod
    def get_all(status: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[Report]:
        """Get all reports, optionally filtered by status."""
        offset = (page - 1) * page_size
        query = Report.objects.select_related('reporter', 'resolved_by')
        if status:
            query = query.filter(status=status)
        return query.order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def update_status(report_id: str, status: str, resolved_by_id: Optional[str] = None) -> Optional[Report]:
        """Update report status."""
        try:
            report = Report.objects.get(report_id=report_id)
            report.status = status
            if resolved_by_id:
                report.resolved_by_id = resolved_by_id
            if status in ['resolved', 'rejected']:
                from django.utils import timezone
                report.resolved_at = timezone.now()
            report.save()
            return report
        except Report.DoesNotExist:
            return None


class AuditLogRepository:
    """Repository for AuditLog entity operations."""
    
    @staticmethod
    def create(user_id: Optional[str], action_type: str, resource_type: str,
               resource_id: Optional[str] = None, details: Optional[str] = None,
               ip_address: Optional[str] = None) -> AuditLog:
        """Create a new audit log entry."""
        return AuditLog.objects.create(
            user_id=user_id,
            action_type=action_type,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
    
    @staticmethod
    def get_by_user(user_id: str, page: int = 1, page_size: int = 20) -> List[AuditLog]:
        """Get audit logs for a user."""
        offset = (page - 1) * page_size
        return AuditLog.objects.filter(user_id=user_id).order_by('-created_at')[offset:offset + page_size]
    
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20) -> List[AuditLog]:
        """Get all audit logs."""
        offset = (page - 1) * page_size
        return AuditLog.objects.select_related('user').order_by('-created_at')[offset:offset + page_size]


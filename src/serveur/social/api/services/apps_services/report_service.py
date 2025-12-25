"""
Report and moderation service.
"""
from typing import List, Optional, Tuple
from django.db import transaction
from db.repositories.message_repository import ReportRepository, AuditLogRepository
from db.repositories.user_repository import UserRepository
from db.repositories.post_repository import PostRepository, CommentRepository
from db.entities.message_entity import Report
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError


class ReportService:
    """Service for reporting and moderation."""
    
    @staticmethod
    @transaction.atomic
    def create_report(
        reporter_id: str,
        target_type: str,
        target_id: str,
        reason: str,
        ip_address: Optional[str] = None
    ) -> Report:
        """
        Create a report.
        
        Args:
            reporter_id: Reporter user ID
            target_type: Type of target (post, comment, user)
            target_id: Target ID
            reason: Report reason
            ip_address: Client IP address
            
        Returns:
            Created report
        """
        # Validate target type
        if target_type not in ['post', 'comment', 'user']:
            raise ValidationError(f"Invalid target type: {target_type}")
        
        # Validate reason length
        if not reason or len(reason) < 10:
            raise ValidationError("Reason must be at least 10 characters")
        if len(reason) > 500:
            raise ValidationError("Reason must be at most 500 characters")
        
        # Check if target exists
        if target_type == 'post':
            target = PostRepository.get_by_id(target_id)
            if not target:
                raise NotFoundError(f"Post {target_id} not found")
        elif target_type == 'comment':
            target = CommentRepository.get_by_id(target_id)
            if not target:
                raise NotFoundError(f"Comment {target_id} not found")
        elif target_type == 'user':
            target = UserRepository.get_by_id(target_id)
            if not target:
                raise NotFoundError(f"User {target_id} not found")
            # Cannot report yourself
            if target_id == reporter_id:
                raise ValidationError("Cannot report yourself")
        
        # Create report
        report = ReportRepository.create(
            reporter_id=reporter_id,
            target_type=target_type,
            target_id=target_id,
            reason=reason
        )
        
        # Audit log
        AuditLogRepository.create(
            user_id=reporter_id,
            action_type='report_created',
            resource_type='report',
            resource_id=str(report.report_id),
            details={'target_type': target_type, 'target_id': target_id},
            ip_address=ip_address
        )
        
        return report
    
    @staticmethod
    def get_report_by_id(report_id: str) -> Report:
        """Get report by ID."""
        report = ReportRepository.get_by_id(report_id)
        if not report:
            raise NotFoundError(f"Report {report_id} not found")
        return report
    
    @staticmethod
    def get_all_reports(
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Report], int]:
        """
        Get all reports (admin only).
        
        Args:
            status: Filter by status (pending, under_review, resolved, rejected)
            page: Page number
            page_size: Page size
            
        Returns:
            Tuple of (reports, total_count)
        """
        return ReportRepository.get_all(status, page, page_size)
    
    @staticmethod
    @transaction.atomic
    def update_report_status(
        report_id: str,
        admin_id: str,
        status: str,
        ip_address: Optional[str] = None,
        action_details: Optional[dict] = None
    ) -> Report:
        """
        Update report status (admin only).
        
        Args:
            report_id: Report ID
            admin_id: Admin user ID
            status: New status (under_review, resolved, rejected)
            ip_address: Client IP address
            
        Returns:
            Updated report
        """
        # Validate status
        if status not in ['under_review', 'resolved', 'rejected']:
            raise ValidationError(f"Invalid status: {status}")
        
        # Check if admin
        admin = UserRepository.get_by_id(admin_id)
        if not admin or not admin.is_admin:
            raise PermissionDeniedError("Admin access required")
        
        # Update report
        report = ReportService.get_report_by_id(report_id)
        resolved_by_id = admin_id if status in ['resolved', 'rejected'] else None
        report = ReportRepository.update_status(report_id, status, resolved_by_id=resolved_by_id)
        
        # Audit log
        AuditLogRepository.create(
            user_id=admin_id,
            action_type='resolve_report',
            resource_type='report',
            resource_id=report_id,
            details={'status': status, 'action': action_details or {}},
            ip_address=ip_address
        )
        
        return report
    
    @staticmethod
    @transaction.atomic
    def ban_user(
        admin_id: str,
        user_id: str,
        ip_address: Optional[str] = None
    ) -> None:
        """
        Ban a user (admin only).
        
        Args:
            admin_id: Admin user ID
            user_id: User ID to ban
            ip_address: Client IP address
        """
        # Check if admin
        admin = UserRepository.get_by_id(admin_id)
        if not admin or not admin.is_admin:
            raise PermissionDeniedError("Admin access required")
        
        # Cannot ban yourself
        if admin_id == user_id:
            raise ValidationError("Cannot ban yourself")
        
        # Get user
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User {user_id} not found")
        
        # Ban user
        user.is_banned = True
        user.save()
        
        # Audit log
        AuditLogRepository.create(
            user_id=admin_id,
            action_type='user_banned',
            resource_type='user',
            resource_id=user_id,
            ip_address=ip_address
        )

    @staticmethod
    @transaction.atomic
    def unban_user(
        admin_id: str,
        user_id: str,
        ip_address: Optional[str] = None
    ) -> None:
        """
        Unban a user (admin only).

        Args:
            admin_id: Admin user ID
            user_id: User ID to unban
            ip_address: Client IP address
        """
        # Check if admin
        admin = UserRepository.get_by_id(admin_id)
        if not admin or not admin.is_admin:
            raise PermissionDeniedError("Admin access required")

        # Get user
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User {user_id} not found")

        # Unban user
        user.is_banned = False
        user.save()

        # Audit log
        AuditLogRepository.create(
            user_id=admin_id,
            action_type='user_unbanned',
            resource_type='user',
            resource_id=user_id,
            ip_address=ip_address
        )


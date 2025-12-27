"""
Unit tests for ReportService.
Tests business logic with mocked dependencies.
"""
import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from django.utils import timezone
from services.apps_services.report_service import ReportService
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError


# Valid UUIDs for tests
TEST_UUID_REPORTER = str(uuid.uuid4())
TEST_UUID_ADMIN = str(uuid.uuid4())
TEST_UUID_TARGET = str(uuid.uuid4())
TEST_UUID_REPORT = str(uuid.uuid4())


@pytest.fixture
def mock_report():
    """Mock Report object."""
    report = Mock()
    report.report_id = TEST_UUID_REPORT
    report.reporter_id = TEST_UUID_REPORTER
    report.target_type = 'post'
    report.target_id = TEST_UUID_TARGET
    report.reason = 'spam'
    report.description = 'This is spam content'
    report.status = 'pending'
    report.resolved_by_id = None
    report.created_at = datetime.now()
    report.resolved_at = None
    return report


@pytest.mark.django_db
class TestReportServiceCreateReport:
    """Test ReportService.create_report() method."""

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.PostRepository')
    def test_create_report_on_post_success(self, mock_post_repo, mock_report_repo, mock_audit):
        """Test creating a report on a post successfully."""
        # Setup mocks
        mock_post = Mock()
        mock_post.post_id = TEST_UUID_TARGET
        mock_post_repo.get_by_id.return_value = mock_post

        mock_created_report = Mock()
        mock_created_report.report_id = TEST_UUID_REPORT
        mock_report_repo.create.return_value = mock_created_report

        # Call service
        result = ReportService.create_report(
            reporter_id=TEST_UUID_REPORTER,
            target_type='post',
            target_id=TEST_UUID_TARGET,
            reason='This is spam content that violates guidelines',
            ip_address='127.0.0.1'
        )

        # Verify
        mock_post_repo.get_by_id.assert_called_once_with(TEST_UUID_TARGET)
        mock_report_repo.create.assert_called_once_with(
            reporter_id=TEST_UUID_REPORTER,
            target_type='post',
            target_id=TEST_UUID_TARGET,
            reason='This is spam content that violates guidelines'
        )
        mock_audit.create.assert_called_once()
        assert result.report_id == TEST_UUID_REPORT

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.CommentRepository')
    def test_create_report_on_comment_success(self, mock_comment_repo, mock_report_repo, mock_audit):
        """Test creating a report on a comment successfully."""
        # Setup mocks
        mock_comment = Mock()
        mock_comment.comment_id = TEST_UUID_TARGET
        mock_comment_repo.get_by_id.return_value = mock_comment

        mock_created_report = Mock()
        mock_created_report.report_id = TEST_UUID_REPORT
        mock_report_repo.create.return_value = mock_created_report

        # Call service
        result = ReportService.create_report(
            reporter_id=TEST_UUID_REPORTER,
            target_type='comment',
            target_id=TEST_UUID_TARGET,
            reason='Harassment in comment that needs moderation',
            ip_address='127.0.0.1'
        )

        # Verify
        mock_comment_repo.get_by_id.assert_called_once_with(TEST_UUID_TARGET)
        mock_report_repo.create.assert_called_once()
        assert result.report_id == TEST_UUID_REPORT

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_create_report_on_user_success(self, mock_user_repo, mock_report_repo, mock_audit):
        """Test creating a report on a user successfully."""
        # Setup mocks
        mock_user = Mock()
        mock_user.user_id = TEST_UUID_TARGET
        mock_user_repo.get_by_id.return_value = mock_user

        mock_created_report = Mock()
        mock_created_report.report_id = TEST_UUID_REPORT
        mock_report_repo.create.return_value = mock_created_report

        # Call service
        result = ReportService.create_report(
            reporter_id=TEST_UUID_REPORTER,
            target_type='user',
            target_id=TEST_UUID_TARGET,
            reason='User spreading misinformation across platform',
            ip_address='127.0.0.1'
        )

        # Verify
        mock_user_repo.get_by_id.assert_called_once_with(TEST_UUID_TARGET)
        mock_report_repo.create.assert_called_once()
        assert result.report_id == TEST_UUID_REPORT

    def test_create_report_invalid_target_type(self):
        """Test creating report with invalid target type fails."""
        with pytest.raises(ValidationError, match="Invalid target type"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='invalid_type',
                target_id=TEST_UUID_TARGET,
                reason='Valid reason with enough characters',
                ip_address='127.0.0.1'
            )

    def test_create_report_reason_too_short(self):
        """Test creating report with too short reason fails."""
        with pytest.raises(ValidationError, match="Reason must be at least 10 characters"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='post',
                target_id=TEST_UUID_TARGET,
                reason='short',
                ip_address='127.0.0.1'
            )

    def test_create_report_reason_too_long(self):
        """Test creating report with too long reason fails."""
        long_reason = 'x' * 501
        with pytest.raises(ValidationError, match="Reason must be at most 500 characters"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='post',
                target_id=TEST_UUID_TARGET,
                reason=long_reason,
                ip_address='127.0.0.1'
            )

    def test_create_report_empty_reason(self):
        """Test creating report with empty reason fails."""
        with pytest.raises(ValidationError, match="Reason must be at least 10 characters"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='post',
                target_id=TEST_UUID_TARGET,
                reason='',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.PostRepository')
    def test_create_report_nonexistent_post(self, mock_post_repo):
        """Test creating report on non-existent post fails."""
        mock_post_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Post .* not found"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='post',
                target_id=TEST_UUID_TARGET,
                reason='Valid reason for reporting',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.CommentRepository')
    def test_create_report_nonexistent_comment(self, mock_comment_repo):
        """Test creating report on non-existent comment fails."""
        mock_comment_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Comment .* not found"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='comment',
                target_id=TEST_UUID_TARGET,
                reason='Valid reason for reporting',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.UserRepository')
    def test_create_report_nonexistent_user(self, mock_user_repo):
        """Test creating report on non-existent user fails."""
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="User .* not found"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='user',
                target_id=TEST_UUID_TARGET,
                reason='Valid reason for reporting',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.UserRepository')
    def test_create_report_on_self_fails(self, mock_user_repo):
        """Test user cannot report themselves."""
        mock_user = Mock()
        mock_user.user_id = TEST_UUID_REPORTER
        mock_user_repo.get_by_id.return_value = mock_user

        with pytest.raises(ValidationError, match="Cannot report yourself"):
            ReportService.create_report(
                reporter_id=TEST_UUID_REPORTER,
                target_type='user',
                target_id=TEST_UUID_REPORTER,
                reason='Trying to report myself',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.PostRepository')
    def test_create_report_creates_audit_log(self, mock_post_repo, mock_report_repo, mock_audit):
        """Test creating report creates audit log."""
        mock_post = Mock()
        mock_post_repo.get_by_id.return_value = mock_post
        mock_report = Mock()
        mock_report.report_id = TEST_UUID_REPORT
        mock_report_repo.create.return_value = mock_report

        ReportService.create_report(
            reporter_id=TEST_UUID_REPORTER,
            target_type='post',
            target_id=TEST_UUID_TARGET,
            reason='Valid reason for reporting content',
            ip_address='192.168.1.1'
        )

        # Verify audit log was created
        call_args = mock_audit.create.call_args
        assert call_args[1]['user_id'] == TEST_UUID_REPORTER
        assert call_args[1]['action_type'] == 'report_created'
        assert call_args[1]['resource_type'] == 'report'
        assert call_args[1]['resource_id'] == str(TEST_UUID_REPORT)
        assert call_args[1]['ip_address'] == '192.168.1.1'


@pytest.mark.django_db
class TestReportServiceGetReport:
    """Test ReportService.get_report_by_id() method."""

    @patch('services.apps_services.report_service.ReportRepository')
    def test_get_report_by_id_success(self, mock_report_repo, mock_report):
        """Test getting report by ID successfully."""
        mock_report_repo.get_by_id.return_value = mock_report

        result = ReportService.get_report_by_id(TEST_UUID_REPORT)

        assert result == mock_report
        mock_report_repo.get_by_id.assert_called_once_with(TEST_UUID_REPORT)

    @patch('services.apps_services.report_service.ReportRepository')
    def test_get_report_by_id_not_found(self, mock_report_repo):
        """Test getting non-existent report fails."""
        mock_report_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Report .* not found"):
            ReportService.get_report_by_id(TEST_UUID_REPORT)


@pytest.mark.django_db
class TestReportServiceGetAllReports:
    """Test ReportService.get_all_reports() method."""

    @patch('services.apps_services.report_service.ReportRepository')
    def test_get_all_reports_success(self, mock_report_repo):
        """Test getting all reports successfully."""
        mock_reports = [Mock(), Mock(), Mock()]
        mock_report_repo.get_all.return_value = (mock_reports, 3)

        reports, total = ReportService.get_all_reports()

        assert len(reports) == 3
        assert total == 3
        mock_report_repo.get_all.assert_called_once_with(None, 1, 20)

    @patch('services.apps_services.report_service.ReportRepository')
    def test_get_all_reports_filtered_by_status(self, mock_report_repo):
        """Test filtering reports by status."""
        mock_reports = [Mock()]
        mock_report_repo.get_all.return_value = (mock_reports, 1)

        reports, total = ReportService.get_all_reports(status='pending')

        assert len(reports) == 1
        mock_report_repo.get_all.assert_called_once_with('pending', 1, 20)

    @patch('services.apps_services.report_service.ReportRepository')
    def test_get_all_reports_with_pagination(self, mock_report_repo):
        """Test getting reports with pagination."""
        mock_reports = [Mock()] * 10
        mock_report_repo.get_all.return_value = (mock_reports, 50)

        reports, total = ReportService.get_all_reports(page=2, page_size=10)

        assert len(reports) == 10
        assert total == 50
        mock_report_repo.get_all.assert_called_once_with(None, 2, 10)

    @patch('services.apps_services.report_service.ReportRepository')
    def test_get_all_reports_empty(self, mock_report_repo):
        """Test getting reports when none exist."""
        mock_report_repo.get_all.return_value = ([], 0)

        reports, total = ReportService.get_all_reports()

        assert len(reports) == 0
        assert total == 0


@pytest.mark.django_db
class TestReportServiceUpdateReportStatus:
    """Test ReportService.update_report_status() method."""

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_update_report_status_to_resolved(self, mock_user_repo, mock_report_repo, mock_audit, mock_report):
        """Test updating report status to resolved."""
        # Setup mocks
        mock_admin = Mock()
        mock_admin.user_id = TEST_UUID_ADMIN
        mock_admin.is_admin = True
        mock_user_repo.get_by_id.return_value = mock_admin

        mock_report.status = 'pending'
        mock_report_repo.get_by_id.return_value = mock_report

        mock_updated_report = Mock()
        mock_updated_report.status = 'resolved'
        mock_report_repo.update_status.return_value = mock_updated_report

        # Call service
        result = ReportService.update_report_status(
            report_id=TEST_UUID_REPORT,
            admin_id=TEST_UUID_ADMIN,
            status='resolved',
            ip_address='127.0.0.1'
        )

        # Verify
        mock_user_repo.get_by_id.assert_called_once_with(TEST_UUID_ADMIN)
        mock_report_repo.update_status.assert_called_once_with(
            TEST_UUID_REPORT,
            'resolved',
            resolved_by_id=TEST_UUID_ADMIN
        )
        mock_audit.create.assert_called_once()
        assert result.status == 'resolved'

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_update_report_status_to_rejected(self, mock_user_repo, mock_report_repo, mock_audit, mock_report):
        """Test updating report status to rejected."""
        mock_admin = Mock()
        mock_admin.is_admin = True
        mock_user_repo.get_by_id.return_value = mock_admin

        mock_report_repo.get_by_id.return_value = mock_report

        mock_updated_report = Mock()
        mock_updated_report.status = 'rejected'
        mock_report_repo.update_status.return_value = mock_updated_report

        result = ReportService.update_report_status(
            report_id=TEST_UUID_REPORT,
            admin_id=TEST_UUID_ADMIN,
            status='rejected',
            ip_address='127.0.0.1'
        )

        assert result.status == 'rejected'

    @patch('services.apps_services.report_service.UserRepository')
    def test_update_report_status_invalid_status(self, mock_user_repo):
        """Test updating report with invalid status fails."""
        mock_admin = Mock()
        mock_admin.is_admin = True
        mock_user_repo.get_by_id.return_value = mock_admin

        with pytest.raises(ValidationError, match="Invalid status"):
            ReportService.update_report_status(
                report_id=TEST_UUID_REPORT,
                admin_id=TEST_UUID_ADMIN,
                status='invalid_status',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.UserRepository')
    def test_update_report_status_non_admin_fails(self, mock_user_repo):
        """Test non-admin cannot update report status."""
        mock_user = Mock()
        mock_user.is_admin = False
        mock_user_repo.get_by_id.return_value = mock_user

        with pytest.raises(PermissionDeniedError, match="Admin access required"):
            ReportService.update_report_status(
                report_id=TEST_UUID_REPORT,
                admin_id=TEST_UUID_REPORTER,
                status='resolved',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.UserRepository')
    def test_update_report_status_nonexistent_admin(self, mock_user_repo):
        """Test updating report with non-existent admin fails."""
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(PermissionDeniedError, match="Admin access required"):
            ReportService.update_report_status(
                report_id=TEST_UUID_REPORT,
                admin_id='nonexistent-id',
                status='resolved',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_update_report_creates_audit_log(self, mock_user_repo, mock_report_repo, mock_audit, mock_report):
        """Test updating report creates audit log."""
        mock_admin = Mock()
        mock_admin.is_admin = True
        mock_user_repo.get_by_id.return_value = mock_admin

        mock_report_repo.get_by_id.return_value = mock_report
        mock_report_repo.update_status.return_value = mock_report

        action_details = {'action': 'content_removed', 'notes': 'Content removed'}

        ReportService.update_report_status(
            report_id=TEST_UUID_REPORT,
            admin_id=TEST_UUID_ADMIN,
            status='resolved',
            ip_address='192.168.1.1',
            action_details=action_details
        )

        # Verify audit log
        call_args = mock_audit.create.call_args
        assert call_args[1]['user_id'] == TEST_UUID_ADMIN
        assert call_args[1]['action_type'] == 'resolve_report'
        assert call_args[1]['resource_type'] == 'report'
        assert call_args[1]['ip_address'] == '192.168.1.1'
        assert 'status' in call_args[1]['details']


@pytest.mark.django_db
class TestReportServiceBanUser:
    """Test ReportService.ban_user() method."""

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_ban_user_success(self, mock_user_repo, mock_audit):
        """Test banning a user successfully."""
        # Setup mocks
        mock_admin = Mock()
        mock_admin.user_id = TEST_UUID_ADMIN
        mock_admin.is_admin = True

        mock_user = Mock()
        mock_user.user_id = TEST_UUID_REPORTER
        mock_user.is_banned = False

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            elif user_id == TEST_UUID_REPORTER:
                return mock_user
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        # Call service
        ReportService.ban_user(
            admin_id=TEST_UUID_ADMIN,
            user_id=TEST_UUID_REPORTER,
            ip_address='127.0.0.1'
        )

        # Verify
        assert mock_user.is_banned == True
        mock_user.save.assert_called_once()
        mock_audit.create.assert_called_once()

    @patch('services.apps_services.report_service.UserRepository')
    def test_ban_user_non_admin_fails(self, mock_user_repo):
        """Test non-admin cannot ban users."""
        mock_user = Mock()
        mock_user.is_admin = False
        mock_user_repo.get_by_id.return_value = mock_user

        with pytest.raises(PermissionDeniedError, match="Admin access required"):
            ReportService.ban_user(
                admin_id=TEST_UUID_REPORTER,
                user_id=TEST_UUID_TARGET,
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.UserRepository')
    def test_ban_self_fails(self, mock_user_repo):
        """Test admin cannot ban themselves."""
        mock_admin = Mock()
        mock_admin.is_admin = True
        mock_user_repo.get_by_id.return_value = mock_admin

        with pytest.raises(ValidationError, match="Cannot ban yourself"):
            ReportService.ban_user(
                admin_id=TEST_UUID_ADMIN,
                user_id=TEST_UUID_ADMIN,
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.UserRepository')
    def test_ban_nonexistent_user_fails(self, mock_user_repo):
        """Test banning non-existent user fails."""
        mock_admin = Mock()
        mock_admin.is_admin = True

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        with pytest.raises(NotFoundError, match="User .* not found"):
            ReportService.ban_user(
                admin_id=TEST_UUID_ADMIN,
                user_id=TEST_UUID_TARGET,
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_ban_user_creates_audit_log(self, mock_user_repo, mock_audit):
        """Test banning user creates audit log."""
        mock_admin = Mock()
        mock_admin.is_admin = True

        mock_user = Mock()
        mock_user.is_banned = False

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            elif user_id == TEST_UUID_REPORTER:
                return mock_user
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        ReportService.ban_user(
            admin_id=TEST_UUID_ADMIN,
            user_id=TEST_UUID_REPORTER,
            ip_address='192.168.1.1'
        )

        # Verify audit log
        call_args = mock_audit.create.call_args
        assert call_args[1]['user_id'] == TEST_UUID_ADMIN
        assert call_args[1]['action_type'] == 'user_banned'
        assert call_args[1]['resource_type'] == 'user'
        assert call_args[1]['resource_id'] == TEST_UUID_REPORTER
        assert call_args[1]['ip_address'] == '192.168.1.1'


@pytest.mark.django_db
class TestReportServiceUnbanUser:
    """Test ReportService.unban_user() method."""

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_unban_user_success(self, mock_user_repo, mock_audit):
        """Test unbanning a user successfully."""
        mock_admin = Mock()
        mock_admin.is_admin = True

        mock_user = Mock()
        mock_user.is_banned = True

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            elif user_id == TEST_UUID_REPORTER:
                return mock_user
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        ReportService.unban_user(
            admin_id=TEST_UUID_ADMIN,
            user_id=TEST_UUID_REPORTER,
            ip_address='127.0.0.1'
        )

        assert mock_user.is_banned == False
        mock_user.save.assert_called_once()
        mock_audit.create.assert_called_once()

    @patch('services.apps_services.report_service.UserRepository')
    def test_unban_user_non_admin_fails(self, mock_user_repo):
        """Test non-admin cannot unban users."""
        mock_user = Mock()
        mock_user.is_admin = False
        mock_user_repo.get_by_id.return_value = mock_user

        with pytest.raises(PermissionDeniedError, match="Admin access required"):
            ReportService.unban_user(
                admin_id=TEST_UUID_REPORTER,
                user_id=TEST_UUID_TARGET,
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.UserRepository')
    def test_unban_nonexistent_user_fails(self, mock_user_repo):
        """Test unbanning non-existent user fails."""
        mock_admin = Mock()
        mock_admin.is_admin = True

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        with pytest.raises(NotFoundError, match="User .* not found"):
            ReportService.unban_user(
                admin_id=TEST_UUID_ADMIN,
                user_id=TEST_UUID_TARGET,
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_unban_user_creates_audit_log(self, mock_user_repo, mock_audit):
        """Test unbanning user creates audit log."""
        mock_admin = Mock()
        mock_admin.is_admin = True

        mock_user = Mock()
        mock_user.is_banned = True

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            elif user_id == TEST_UUID_REPORTER:
                return mock_user
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        ReportService.unban_user(
            admin_id=TEST_UUID_ADMIN,
            user_id=TEST_UUID_REPORTER,
            ip_address='192.168.1.1'
        )

        # Verify audit log
        call_args = mock_audit.create.call_args
        assert call_args[1]['user_id'] == TEST_UUID_ADMIN
        assert call_args[1]['action_type'] == 'user_unbanned'
        assert call_args[1]['resource_type'] == 'user'
        assert call_args[1]['resource_id'] == TEST_UUID_REPORTER
        assert call_args[1]['ip_address'] == '192.168.1.1'


@pytest.mark.django_db
class TestReportServiceEdgeCases:
    """Test edge cases and error handling."""

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.PostRepository')
    def test_create_report_with_special_characters(self, mock_post_repo, mock_report_repo, mock_audit):
        """Test creating report with special unicode characters."""
        special_reason = "This contains special chars: 你好 🎉 \n\t <>&\"' and more"

        mock_post = Mock()
        mock_post_repo.get_by_id.return_value = mock_post
        mock_report = Mock()
        mock_report.report_id = TEST_UUID_REPORT
        mock_report_repo.create.return_value = mock_report

        result = ReportService.create_report(
            reporter_id=TEST_UUID_REPORTER,
            target_type='post',
            target_id=TEST_UUID_TARGET,
            reason=special_reason,
            ip_address='127.0.0.1'
        )

        assert result is not None

    @patch('services.apps_services.report_service.ReportRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_update_report_status_pending_not_allowed(self, mock_user_repo, mock_report_repo):
        """Test cannot update report status to pending (only resolved/rejected/under_review)."""
        mock_admin = Mock()
        mock_admin.is_admin = True
        mock_user_repo.get_by_id.return_value = mock_admin

        with pytest.raises(ValidationError, match="Invalid status"):
            ReportService.update_report_status(
                report_id=TEST_UUID_REPORT,
                admin_id=TEST_UUID_ADMIN,
                status='pending',
                ip_address='127.0.0.1'
            )

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_ban_already_banned_user(self, mock_user_repo, mock_audit):
        """Test banning already banned user (idempotent)."""
        mock_admin = Mock()
        mock_admin.is_admin = True

        mock_user = Mock()
        mock_user.is_banned = True  # Already banned

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            elif user_id == TEST_UUID_REPORTER:
                return mock_user
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        # Should succeed (idempotent)
        ReportService.ban_user(
            admin_id=TEST_UUID_ADMIN,
            user_id=TEST_UUID_REPORTER,
            ip_address='127.0.0.1'
        )

        assert mock_user.is_banned == True

    @patch('services.apps_services.report_service.AuditLogRepository')
    @patch('services.apps_services.report_service.UserRepository')
    def test_unban_not_banned_user(self, mock_user_repo, mock_audit):
        """Test unbanning user who is not banned (idempotent)."""
        mock_admin = Mock()
        mock_admin.is_admin = True

        mock_user = Mock()
        mock_user.is_banned = False  # Not banned

        def get_by_id_side_effect(user_id):
            if user_id == TEST_UUID_ADMIN:
                return mock_admin
            elif user_id == TEST_UUID_REPORTER:
                return mock_user
            return None

        mock_user_repo.get_by_id.side_effect = get_by_id_side_effect

        # Should succeed (idempotent)
        ReportService.unban_user(
            admin_id=TEST_UUID_ADMIN,
            user_id=TEST_UUID_REPORTER,
            ip_address='127.0.0.1'
        )

        assert mock_user.is_banned == False

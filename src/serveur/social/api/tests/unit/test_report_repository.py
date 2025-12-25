"""
Unit tests for ReportRepository.
Tests database operations for reports.
"""
import pytest
from django.utils import timezone
from db.repositories.message_repository import ReportRepository
from db.entities.message_entity import Report
from db.entities.user_entity import User, UserProfile, UserSettings
from db.entities.post_entity import Post
from db.entities.domain_entity import Domain, Subforum


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.objects.create(
        email='reporter@test.com',
        username='reporter',
        firebase_uid='firebase_reporter'
    )
    UserProfile.objects.create(user=user, display_name='Reporter')
    UserSettings.objects.create(user=user)
    return user


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User.objects.create(
        email='admin@test.com',
        username='admin',
        firebase_uid='firebase_admin',
        is_admin=True
    )
    UserProfile.objects.create(user=user, display_name='Admin')
    UserSettings.objects.create(user=user)
    return user


@pytest.fixture
def test_domain(db):
    """Create a test domain."""
    return Domain.objects.create(
        domain_name='Test Domain',
        description='Test domain description'
    )


@pytest.fixture
def test_subforum(db, test_domain):
    """Create a test subforum."""
    return Subforum.objects.create(
        subforum_name='Test Subforum',
        domain=test_domain,
        description='Test subforum description'
    )


@pytest.fixture
def test_post(db, test_user, test_subforum):
    """Create a test post."""
    return Post.objects.create(
        user=test_user,
        subforum=test_subforum,
        title='Test Post',
        content='Test post content'
    )


@pytest.mark.django_db
class TestReportRepositoryCreate:
    """Test ReportRepository.create() method."""

    def test_create_report_success(self, test_user, test_post):
        """Test creating a report successfully."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam',
            description='This is spam content'
        )

        assert report is not None
        assert report.reporter == test_user
        assert report.target_type == 'post'
        assert str(report.target_id) == str(test_post.post_id)
        assert report.reason == 'spam'
        assert report.description == 'This is spam content'
        assert report.status == 'pending'
        assert report.resolved_by is None
        assert report.resolved_at is None
        assert report.created_at is not None

    def test_create_report_without_description(self, test_user, test_post):
        """Test creating report without description."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='harassment'
        )

        assert report is not None
        assert report.description is None

    def test_create_multiple_reports_same_target(self, test_user, test_post):
        """Test creating multiple reports on same target."""
        report1 = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        report2 = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='inappropriate'
        )

        assert report1.report_id != report2.report_id
        assert Report.objects.filter(target_id=test_post.post_id).count() == 2


@pytest.mark.django_db
class TestReportRepositoryGetById:
    """Test ReportRepository.get_by_id() method."""

    def test_get_report_by_id_success(self, test_user, test_post):
        """Test getting report by ID successfully."""
        created_report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        retrieved_report = ReportRepository.get_by_id(str(created_report.report_id))

        assert retrieved_report is not None
        assert retrieved_report.report_id == created_report.report_id
        assert retrieved_report.reporter == test_user

    def test_get_report_by_id_not_found(self):
        """Test getting non-existent report returns None."""
        report = ReportRepository.get_by_id('00000000-0000-0000-0000-000000000000')

        assert report is None

    def test_get_report_includes_related_objects(self, test_user, admin_user, test_post):
        """Test that get_by_id includes reporter and resolved_by."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        # Update report with resolver
        report.status = 'resolved'
        report.resolved_by = admin_user
        report.resolved_at = timezone.now()
        report.save()

        retrieved_report = ReportRepository.get_by_id(str(report.report_id))

        assert retrieved_report.reporter == test_user
        assert retrieved_report.resolved_by == admin_user


@pytest.mark.django_db
class TestReportRepositoryGetAll:
    """Test ReportRepository.get_all() method."""

    def test_get_all_reports(self, test_user, test_post):
        """Test getting all reports."""
        # Create multiple reports
        ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )
        ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='harassment'
        )

        reports, total = ReportRepository.get_all()

        assert len(reports) >= 2
        assert total >= 2

    def test_get_all_reports_filtered_by_status(self, test_user, test_post):
        """Test filtering reports by status."""
        # Create reports with different statuses
        report1 = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )
        report1.status = 'pending'
        report1.save()

        report2 = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='harassment'
        )
        report2.status = 'resolved'
        report2.save()

        # Get pending reports
        pending_reports, pending_total = ReportRepository.get_all(status='pending')
        assert all(r.status == 'pending' for r in pending_reports)

        # Get resolved reports
        resolved_reports, resolved_total = ReportRepository.get_all(status='resolved')
        assert all(r.status == 'resolved' for r in resolved_reports)

    def test_get_all_reports_pagination(self, test_user, test_post):
        """Test pagination of reports."""
        # Create 25 reports
        for i in range(25):
            ReportRepository.create(
                reporter_id=str(test_user.user_id),
                target_type='post',
                target_id=str(test_post.post_id),
                reason='spam',
                description=f'Report {i}'
            )

        # Get first page
        page1_reports, total = ReportRepository.get_all(page=1, page_size=10)
        assert len(page1_reports) == 10
        assert total >= 25

        # Get second page
        page2_reports, _ = ReportRepository.get_all(page=2, page_size=10)
        assert len(page2_reports) == 10

        # Verify different reports on each page
        page1_ids = {r.report_id for r in page1_reports}
        page2_ids = {r.report_id for r in page2_reports}
        assert page1_ids.isdisjoint(page2_ids)

    def test_get_all_reports_ordered_by_created_at(self, test_user, test_post):
        """Test reports are ordered by created_at descending."""
        # Create reports
        report1 = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        report2 = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='harassment'
        )

        reports, _ = ReportRepository.get_all()

        # Most recent should be first
        assert reports[0].created_at >= reports[-1].created_at

    def test_get_all_reports_empty(self):
        """Test getting reports when none exist."""
        reports, total = ReportRepository.get_all()

        assert reports == [] or len(reports) == 0
        assert total == 0


@pytest.mark.django_db
class TestReportRepositoryUpdateStatus:
    """Test ReportRepository.update_status() method."""

    def test_update_status_to_resolved(self, test_user, admin_user, test_post):
        """Test updating report status to resolved."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        updated_report = ReportRepository.update_status(
            report_id=str(report.report_id),
            status='resolved',
            resolved_by_id=str(admin_user.user_id)
        )

        assert updated_report is not None
        assert updated_report.status == 'resolved'
        assert updated_report.resolved_by == admin_user
        assert updated_report.resolved_at is not None

    def test_update_status_to_rejected(self, test_user, admin_user, test_post):
        """Test updating report status to rejected."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        updated_report = ReportRepository.update_status(
            report_id=str(report.report_id),
            status='rejected',
            resolved_by_id=str(admin_user.user_id)
        )

        assert updated_report.status == 'rejected'
        assert updated_report.resolved_by == admin_user
        assert updated_report.resolved_at is not None

    def test_update_status_without_resolver(self, test_user, test_post):
        """Test updating status without resolved_by."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        # Can update to under_review without resolver
        updated_report = ReportRepository.update_status(
            report_id=str(report.report_id),
            status='under_review'
        )

        assert updated_report.status == 'under_review'

    def test_update_nonexistent_report(self):
        """Test updating non-existent report returns None."""
        result = ReportRepository.update_status(
            report_id='00000000-0000-0000-0000-000000000000',
            status='resolved'
        )

        assert result is None

    def test_update_status_sets_resolved_at(self, test_user, admin_user, test_post):
        """Test that resolved_at is set when status is resolved/rejected."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        assert report.resolved_at is None

        # Update to resolved
        updated_report = ReportRepository.update_status(
            report_id=str(report.report_id),
            status='resolved',
            resolved_by_id=str(admin_user.user_id)
        )

        assert updated_report.resolved_at is not None


@pytest.mark.django_db
class TestReportRepositoryIndexes:
    """Test that database indexes are properly configured."""

    def test_report_has_reporter_index(self):
        """Test that reporter field is indexed."""
        from db.entities.message_entity import Report

        indexes = [idx.fields for idx in Report._meta.indexes]
        assert any('reporter' in idx for idx in indexes)

    def test_report_has_status_index(self):
        """Test that status field is indexed."""
        from db.entities.message_entity import Report

        indexes = [idx.fields for idx in Report._meta.indexes]
        assert any('status' in idx for idx in indexes)

    def test_report_has_target_index(self):
        """Test that target_type and target_id are indexed."""
        from db.entities.message_entity import Report

        indexes = [idx.fields for idx in Report._meta.indexes]
        # Should have composite index on target_type and target_id
        assert any('target_type' in idx and 'target_id' in idx for idx in indexes)


@pytest.mark.django_db
class TestReportRepositoryEdgeCases:
    """Test edge cases and special scenarios."""

    def test_create_report_with_max_length_reason(self, test_user, test_post):
        """Test creating report with maximum length reason."""
        max_reason = 'x' * 500  # Max allowed

        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam',
            description=max_reason
        )

        assert report is not None
        assert len(report.description) == 500

    def test_create_report_different_target_types(self, test_user, test_post):
        """Test creating reports with different target types."""
        # Test post target
        report_post = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )
        assert report_post.target_type == 'post'

        # Test comment target
        report_comment = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='comment',
            target_id=str(test_post.post_id),  # Using post_id as placeholder
            reason='harassment'
        )
        assert report_comment.target_type == 'comment'

        # Test user target
        report_user = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='user',
            target_id=str(test_user.user_id),
            reason='inappropriate'
        )
        assert report_user.target_type == 'user'

    def test_get_all_with_large_page_size(self, test_user, test_post):
        """Test getting all reports with very large page size."""
        # Create some reports
        for i in range(5):
            ReportRepository.create(
                reporter_id=str(test_user.user_id),
                target_type='post',
                target_id=str(test_post.post_id),
                reason='spam'
            )

        reports, total = ReportRepository.get_all(page=1, page_size=1000)

        assert len(reports) >= 5
        assert total >= 5

    def test_update_status_multiple_times(self, test_user, admin_user, test_post):
        """Test updating report status multiple times."""
        report = ReportRepository.create(
            reporter_id=str(test_user.user_id),
            target_type='post',
            target_id=str(test_post.post_id),
            reason='spam'
        )

        # First update
        ReportRepository.update_status(
            report_id=str(report.report_id),
            status='under_review'
        )

        # Second update
        updated = ReportRepository.update_status(
            report_id=str(report.report_id),
            status='resolved',
            resolved_by_id=str(admin_user.user_id)
        )

        assert updated.status == 'resolved'

    def test_get_all_filters_correctly(self, test_user, test_post):
        """Test that status filter works correctly."""
        # Create reports with different statuses
        for i in range(3):
            report = ReportRepository.create(
                reporter_id=str(test_user.user_id),
                target_type='post',
                target_id=str(test_post.post_id),
                reason='spam'
            )
            if i == 0:
                report.status = 'pending'
            elif i == 1:
                report.status = 'resolved'
            else:
                report.status = 'rejected'
            report.save()

        # Get only pending
        pending, _ = ReportRepository.get_all(status='pending')
        assert all(r.status == 'pending' for r in pending)

        # Get only resolved
        resolved, _ = ReportRepository.get_all(status='resolved')
        assert all(r.status == 'resolved' for r in resolved)

        # Get only rejected
        rejected, _ = ReportRepository.get_all(status='rejected')
        assert all(r.status == 'rejected' for r in rejected)

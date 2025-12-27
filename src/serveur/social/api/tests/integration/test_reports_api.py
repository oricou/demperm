"""
Integration tests for Reports API.
Tests report creation, listing, and moderation endpoints.
"""
import pytest
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient
from db.entities.message_entity import Report
from db.entities.user_entity import User, UserProfile, UserSettings
from db.entities.post_entity import Post, Comment
from db.entities.domain_entity import Domain, Subforum


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def regular_user(db):
    """Create a regular test user."""
    user = User.objects.create(
        email='user@test.com',
        username='testuser',
        firebase_uid='firebase_regular'
    )
    UserProfile.objects.create(user=user, display_name='Test User')
    UserSettings.objects.create(user=user)
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def another_user(db):
    """Create another regular user."""
    user = User.objects.create(
        email='user2@test.com',
        username='testuser2',
        firebase_uid='firebase_user2'
    )
    UserProfile.objects.create(user=user, display_name='Test User 2')
    UserSettings.objects.create(user=user)
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User.objects.create(
        email='admin@test.com',
        username='adminuser',
        firebase_uid='firebase_admin',
        is_admin=True
    )
    UserProfile.objects.create(user=user, display_name='Admin User')
    UserSettings.objects.create(user=user)
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def banned_user(db):
    """Create a banned user."""
    user = User.objects.create(
        email='banned@test.com',
        username='banneduser',
        firebase_uid='firebase_banned',
        is_banned=True
    )
    UserProfile.objects.create(user=user, display_name='Banned User')
    UserSettings.objects.create(user=user)
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def test_domain(db):
    """Create a test domain."""
    return Domain.objects.create(
        domain_name='Test Domain',
        description='A test domain'
    )


@pytest.fixture
def test_subforum(db, test_domain):
    """Create a test subforum."""
    return Subforum.objects.create(
        subforum_name='Test Subforum',
        domain=test_domain,
        description='A test subforum'
    )


@pytest.fixture
def test_post(db, regular_user, test_subforum):
    """Create a test post."""
    return Post.objects.create(
        user=regular_user,
        subforum=test_subforum,
        title='Test Post',
        content='This is a test post content'
    )


@pytest.fixture
def test_comment(db, another_user, test_post):
    """Create a test comment."""
    return Comment.objects.create(
        user=another_user,
        post=test_post,
        content='This is a test comment'
    )


@pytest.mark.django_db
class TestCreateReportAPI:
    """Test creating reports."""

    def test_create_report_on_post_success(self, api_client, regular_user, test_post):
        """Test creating a report on a post successfully."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'post',
            'target_id': str(test_post.post_id),
            'reason': 'This post contains spam content that violates community guidelines'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'report_id' in response.data
        assert response.data['target_type'] == 'post'
        assert response.data['target_id'] == str(test_post.post_id)
        assert response.data['status'] == 'pending'

        # Verify report was created in database
        report = Report.objects.get(report_id=response.data['report_id'])
        assert report.reporter == regular_user
        assert report.target_type == 'post'
        assert str(report.target_id) == str(test_post.post_id)

    def test_create_report_on_comment_success(self, api_client, regular_user, test_comment):
        """Test creating a report on a comment."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'comment',
            'target_id': str(test_comment.comment_id),
            'reason': 'This comment is harassment and should be removed from platform'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['target_type'] == 'comment'

    def test_create_report_on_user_success(self, api_client, regular_user, another_user):
        """Test creating a report on a user."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'user',
            'target_id': str(another_user.user_id),
            'reason': 'This user is spreading misinformation across multiple posts'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['target_type'] == 'user'

    def test_create_report_invalid_target_type(self, api_client, regular_user):
        """Test creating report with invalid target type fails."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'invalid_type',
            'target_id': 'some-uuid',
            'reason': 'Some reason that is long enough to pass validation'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_report_short_reason_fails(self, api_client, regular_user, test_post):
        """Test creating report with too short reason fails."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'post',
            'target_id': str(test_post.post_id),
            'reason': 'short'  # Less than 10 characters
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_report_long_reason_fails(self, api_client, regular_user, test_post):
        """Test creating report with too long reason fails."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'post',
            'target_id': str(test_post.post_id),
            'reason': 'x' * 501  # More than 500 characters
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_report_nonexistent_post(self, api_client, regular_user):
        """Test creating report on non-existent post fails."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'post',
            'target_id': '00000000-0000-0000-0000-000000000000',
            'reason': 'This is a valid reason for reporting the content'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_report_on_self_fails(self, api_client, regular_user):
        """Test user cannot report themselves."""
        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'user',
            'target_id': str(regular_user.user_id),
            'reason': 'Trying to report myself which should not be allowed'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_report_unauthenticated_fails(self, api_client, test_post):
        """Test unauthenticated users cannot create reports."""
        payload = {
            'target_type': 'post',
            'target_id': str(test_post.post_id),
            'reason': 'This should fail because user is not authenticated'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    def test_create_report_banned_user_fails(self, api_client, banned_user, test_post):
        """Test banned users cannot create reports."""
        api_client.force_authenticate(user=banned_user)

        payload = {
            'target_type': 'post',
            'target_id': str(test_post.post_id),
            'reason': 'Banned users should not be able to create reports'
        }

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_report_different_reason_types(self, api_client, regular_user, test_post):
        """Test creating reports with different reason types."""
        api_client.force_authenticate(user=regular_user)

        reasons = [
            'This is spam content that should be removed immediately',
            'Harassment and bullying behavior that violates guidelines',
            'Inappropriate content that is not suitable for audience',
            'Misinformation spreading false claims about health',
            'Other reason that does not fit into above categories'
        ]

        for reason in reasons:
            payload = {
                'target_type': 'post',
                'target_id': str(test_post.post_id),
                'reason': reason
            }

            response = api_client.post('/api/v1/reports/create/', payload, format='json')
            assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestAdminReportsListAPI:
    """Test admin reports listing."""

    def test_admin_get_all_reports(self, api_client, admin_user, regular_user, test_post):
        """Test admin can get all reports."""
        # Create some reports
        Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='spam',
            description='This is spam'
        )
        Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='harassment',
            description='Harassment content'
        )

        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/v1/admin/reports/')

        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.data
        assert 'reports' in response.data['data']
        assert len(response.data['data']['reports']) >= 2

    def test_admin_filter_reports_by_status(self, api_client, admin_user, regular_user, test_post):
        """Test admin can filter reports by status."""
        # Create reports with different statuses
        Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='spam',
            description='Spam',
            status='pending'
        )
        Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='harassment',
            description='Harassment',
            status='resolved'
        )

        api_client.force_authenticate(user=admin_user)

        # Filter by pending
        response = api_client.get('/api/v1/admin/reports/?status=pending')
        assert response.status_code == status.HTTP_200_OK
        pending_reports = response.data['data']['reports']
        assert all(r['status'] == 'pending' for r in pending_reports)

        # Filter by resolved
        response = api_client.get('/api/v1/admin/reports/?status=resolved')
        assert response.status_code == status.HTTP_200_OK
        resolved_reports = response.data['data']['reports']
        assert all(r['status'] == 'resolved' for r in resolved_reports)

    def test_admin_reports_pagination(self, api_client, admin_user, regular_user, test_post):
        """Test admin reports list pagination."""
        # Create multiple reports
        for i in range(25):
            Report.objects.create(
                reporter=regular_user,
                target_type='post',
                target_id=test_post.post_id,
                reason=f'spam report number {i} with enough characters',
                description=f'Report {i}'
            )

        api_client.force_authenticate(user=admin_user)

        # Get first page
        response = api_client.get('/api/v1/admin/reports/?page=1&page_size=10')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']['reports']) <= 10
        assert 'pagination' in response.data
        assert response.data['pagination']['page'] == 1
        assert response.data['pagination']['total_items'] >= 25

    def test_non_admin_cannot_list_reports(self, api_client, regular_user):
        """Test regular users cannot list reports."""
        api_client.force_authenticate(user=regular_user)

        response = api_client.get('/api/v1/admin/reports/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_list_reports(self, api_client):
        """Test unauthenticated users cannot list reports."""
        response = api_client.get('/api/v1/admin/reports/')

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestAdminResolveReportAPI:
    """Test admin resolving reports."""

    def test_admin_resolve_report_success(self, api_client, admin_user, regular_user, test_post):
        """Test admin can resolve a report."""
        report = Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='spam',
            description='This is spam',
            status='pending'
        )

        api_client.force_authenticate(user=admin_user)

        payload = {
            'action': 'content_removed',
            'notes': 'Content has been removed'
        }

        response = api_client.post(
            f'/api/v1/admin/reports/{report.report_id}/resolve/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

        # Verify report was updated
        report.refresh_from_db()
        assert report.status == 'resolved'
        assert report.resolved_by == admin_user
        assert report.resolved_at is not None

    def test_admin_reject_report_success(self, api_client, admin_user, regular_user, test_post):
        """Test admin can reject a report."""
        report = Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='spam',
            description='False report',
            status='pending'
        )

        api_client.force_authenticate(user=admin_user)

        payload = {
            'action': 'no_action',
            'notes': 'Report was reviewed and no action is needed'
        }

        response = api_client.post(
            f'/api/v1/admin/reports/{report.report_id}/reject/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

        # Verify report was updated
        report.refresh_from_db()
        assert report.status == 'rejected'
        assert report.resolved_by == admin_user

    def test_non_admin_cannot_resolve_report(self, api_client, regular_user, test_post):
        """Test regular users cannot resolve reports."""
        report = Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='spam',
            description='Spam'
        )

        api_client.force_authenticate(user=regular_user)

        payload = {'action': 'content_removed', 'notes': 'Test'}
        response = api_client.post(
            f'/api/v1/admin/reports/{report.report_id}/resolve/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_resolve_nonexistent_report_fails(self, api_client, admin_user):
        """Test resolving non-existent report fails."""
        api_client.force_authenticate(user=admin_user)

        payload = {'action': 'content_removed', 'notes': 'Test'}
        response = api_client.post(
            '/api/v1/admin/reports/00000000-0000-0000-0000-000000000000/resolve/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestReportModelFields:
    """Test Report model structure and fields."""

    def test_report_has_required_fields(self, db, regular_user, test_post):
        """Test Report model has all required fields."""
        report = Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='spam',
            description='Test description'
        )

        # Verify all required fields exist
        assert hasattr(report, 'report_id')
        assert hasattr(report, 'reporter')
        assert hasattr(report, 'target_type')
        assert hasattr(report, 'target_id')
        assert hasattr(report, 'reason')
        assert hasattr(report, 'description')
        assert hasattr(report, 'status')
        assert hasattr(report, 'resolved_by')
        assert hasattr(report, 'created_at')
        assert hasattr(report, 'resolved_at')

        # Verify defaults
        assert report.status == 'pending'
        assert report.resolved_by is None
        assert report.resolved_at is None

    def test_report_target_type_choices(self):
        """Test Report model has correct target type choices."""
        from db.entities.message_entity import Report

        target_types = [choice[0] for choice in Report.TARGET_TYPE_CHOICES]
        assert 'post' in target_types
        assert 'comment' in target_types
        assert 'user' in target_types

    def test_report_reason_choices(self):
        """Test Report model has correct reason choices."""
        from db.entities.message_entity import Report

        reasons = [choice[0] for choice in Report.REASON_CHOICES]
        assert 'spam' in reasons
        assert 'harassment' in reasons
        assert 'inappropriate' in reasons
        assert 'misinformation' in reasons
        assert 'other' in reasons

    def test_report_status_choices(self):
        """Test Report model has correct status choices."""
        from db.entities.message_entity import Report

        statuses = [choice[0] for choice in Report.STATUS_CHOICES]
        assert 'pending' in statuses
        assert 'resolved' in statuses
        assert 'rejected' in statuses


@pytest.mark.django_db
class TestReportAuditLogging:
    """Test audit logging for report actions."""

    def test_create_report_creates_audit_log(self, api_client, regular_user, test_post):
        """Test creating report creates audit log entry."""
        from db.entities.message_entity import AuditLog

        api_client.force_authenticate(user=regular_user)

        payload = {
            'target_type': 'post',
            'target_id': str(test_post.post_id),
            'reason': 'This is a spam post that violates community guidelines'
        }

        initial_count = AuditLog.objects.count()

        response = api_client.post('/api/v1/reports/create/', payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        # Verify audit log was created
        assert AuditLog.objects.count() == initial_count + 1

        audit_log = AuditLog.objects.latest('created_at')
        assert audit_log.user == regular_user
        assert audit_log.action_type == 'report_created'
        assert audit_log.resource_type == 'report'

    def test_resolve_report_creates_audit_log(self, api_client, admin_user, regular_user, test_post):
        """Test resolving report creates audit log entry."""
        from db.entities.message_entity import AuditLog

        report = Report.objects.create(
            reporter=regular_user,
            target_type='post',
            target_id=test_post.post_id,
            reason='spam',
            description='Spam content'
        )

        api_client.force_authenticate(user=admin_user)

        initial_count = AuditLog.objects.count()

        payload = {'action': 'content_removed', 'notes': 'Content removed'}
        response = api_client.post(
            f'/api/v1/admin/reports/{report.report_id}/resolve/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

        # Verify audit log was created
        assert AuditLog.objects.count() == initial_count + 1

        audit_log = AuditLog.objects.latest('created_at')
        assert audit_log.user == admin_user
        assert audit_log.action_type == 'resolve_report'

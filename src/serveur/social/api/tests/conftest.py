"""
Pytest configuration and fixtures.
"""
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from db.entities.user_entity import User, UserProfile, UserSettings
from db.entities.domain_entity import Domain


@pytest.fixture
def api_client():
    """Return API client for testing."""
    return APIClient()


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.objects.create(
        firebase_uid='test-firebase-uid',
        email='test@example.com',
        username='testuser'
    )
    UserProfile.objects.create(user=user, display_name='Test User')
    UserSettings.objects.create(user=user)
    return user


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User.objects.create(
        firebase_uid='admin-firebase-uid',
        email='admin@example.com',
        username='adminuser',
        is_admin=True
    )
    UserProfile.objects.create(user=user, display_name='Admin User')
    UserSettings.objects.create(user=user)
    return user


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Return authenticated API client."""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return authenticated admin API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def domains(db):
    """Create test domains."""
    domains_data = [
        {'domain_name': 'Culture', 'description': 'Culture domain'},
        {'domain_name': 'Sport', 'description': 'Sport domain'},
        {'domain_name': 'Environnement', 'description': 'Environment domain'},
    ]
    return [Domain.objects.create(**data) for data in domains_data]


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests."""
    pass

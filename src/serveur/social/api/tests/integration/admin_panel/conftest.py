"""Admin panel test fixtures (inherits shared fixtures from api/tests/conftest)."""
import pytest
from rest_framework.test import APIClient
from db.entities.user_entity import User, UserProfile, UserSettings


@pytest.fixture
def admin_client(api_client, admin_user):
    """
    Authenticated admin client with an `is_authenticated` flag set, so DRF permissions pass.
    """
    admin_user.is_authenticated = True
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def non_admin_client(api_client, test_user):
    """
    Authenticated non-admin client (useful for permission checks).
    """
    test_user.is_authenticated = True
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def banned_client(api_client):
    """
    Authenticated client for a banned user.
    """
    user = User.objects.create(
        firebase_uid="banned-google",
        email="banned@example.com",
        username="banned_user",
        is_banned=True,
    )
    UserProfile.objects.create(user=user, display_name="banned user")
    UserSettings.objects.create(user=user)

    # Use an isolated client to avoid auth being overwritten by other fixtures (e.g., admin_client).
    client = APIClient()
    user.is_authenticated = True
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def another_non_admin(api_client):
    """
    A separate non-admin user for permission tests.
    """
    user = User.objects.create(
        firebase_uid="nonadmin-google",
        email="nonadmin@example.com",
        username="nonadmin_user",
        is_admin=False,
    )
    UserProfile.objects.create(user=user, display_name="nonadmin user")
    UserSettings.objects.create(user=user)
    user.is_authenticated = True
    api_client.force_authenticate(user=user)
    return api_client

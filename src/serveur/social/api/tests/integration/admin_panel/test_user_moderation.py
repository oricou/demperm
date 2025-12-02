"""
Tests for admin user ban/unban endpoints.
"""
import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from db.entities.user_entity import User, UserProfile, UserSettings


def _create_user(email_prefix: str = "user", is_banned: bool = False) -> User:
    """Helper to create a user with profile/settings."""
    suffix = uuid.uuid4()
    user = User.objects.create(
        firebase_uid=f"{email_prefix}-google-{suffix}",
        email=f"{email_prefix}-{suffix}@example.com",
        username=f"{email_prefix}_{suffix}",
        is_banned=is_banned,
    )
    UserProfile.objects.create(user=user, display_name=f"{email_prefix} display")
    UserSettings.objects.create(user=user)
    return user


@pytest.mark.django_db
def test_ban_user_sets_flag(admin_client):
    target = _create_user("ban-target")
    url = reverse("admin_panel:ban-user", args=[target.user_id])

    response = admin_client.post(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    target.refresh_from_db()
    assert target.is_banned is True


@pytest.mark.django_db
def test_ban_user_not_found_returns_400(admin_client):
    url = reverse("admin_panel:ban-user", args=[uuid.uuid4()])

    response = admin_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert body["error"]["code"] == "ERROR"


@pytest.mark.django_db
def test_unban_user_clears_flag(admin_client):
    target = _create_user("unban-target", is_banned=True)
    url = reverse("admin_panel:unban-user", args=[target.user_id])

    response = admin_client.post(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    target.refresh_from_db()
    assert target.is_banned is False


@pytest.mark.django_db
def test_unban_user_not_found_returns_404(admin_client):
    url = reverse("admin_panel:unban-user", args=[uuid.uuid4()])

    response = admin_client.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    body = response.json()
    assert body["error"]["code"] == "NOT_FOUND"


@pytest.mark.django_db
def test_ban_requires_admin(non_admin_client):
    target = _create_user("ban-target")
    url = reverse("admin_panel:ban-user", args=[target.user_id])

    response = non_admin_client.post(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_unban_requires_admin(non_admin_client):
    target = _create_user("unban-target", is_banned=True)
    url = reverse("admin_panel:unban-user", args=[target.user_id])

    response = non_admin_client.post(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

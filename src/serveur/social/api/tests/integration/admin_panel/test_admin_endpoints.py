"""
Additional tests for admin endpoints: domains, tags, stats, post/comment removal.
"""
import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from db.entities.domain_entity import Domain
from db.entities.post_entity import Post, Comment, Tag
from db.entities.user_entity import User, UserProfile, UserSettings


def _mk_user(prefix: str = "user", is_admin: bool = False, banned: bool = False) -> User:
    """Create a user with profile/settings."""
    uid = uuid.uuid4()
    user = User.objects.create(
        firebase_uid=f"{prefix}-google-{uid}",
        email=f"{prefix}-{uid}@example.com",
        username=f"{prefix}_{uid}",
        is_admin=is_admin,
        is_banned=banned,
    )
    UserProfile.objects.create(user=user, display_name=f"{prefix} display")
    UserSettings.objects.create(user=user)
    return user


@pytest.mark.django_db
def test_admin_can_create_and_update_and_delete_domain(admin_client):
    # Create
    create_url = reverse("admin_panel:create-domain")
    resp_create = admin_client.post(
        create_url,
        {"domain_name": "Mobilite", "description": "Desc"},
        format="json",
    )
    assert resp_create.status_code == status.HTTP_201_CREATED
    data = resp_create.json()["data"]
    domain_id = data["domain_id"]
    assert data["domain_name"] == "Mobilite"
    assert "meta" in resp_create.json()

    # Update
    update_url = reverse("admin_panel:update-domain", args=[domain_id])
    resp_update = admin_client.patch(
        update_url,
        {"description": "New desc"},
        format="json",
    )
    assert resp_update.status_code == status.HTTP_200_OK
    updated = resp_update.json()["data"]
    assert updated["description"] == "New desc"

    # Delete
    resp_delete = admin_client.delete(update_url)
    assert resp_delete.status_code == status.HTTP_204_NO_CONTENT
    assert Domain.objects.filter(domain_id=domain_id).count() == 0


@pytest.mark.django_db
def test_delete_tag(admin_client):
    tag = Tag.objects.create(tag_name="politique", creator=_mk_user("creator"))
    url = reverse("admin_panel:delete-tag") + f"?tag_id={tag.tag_id}"
    resp = admin_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert Tag.objects.filter(tag_id=tag.tag_id).count() == 0


@pytest.mark.django_db
def test_delete_tag_validation_error(admin_client):
    url = reverse("admin_panel:delete-tag")  # missing tag_id
    resp = admin_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    body = resp.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.django_db
def test_stats_endpoints_return_meta(admin_client):
    _mk_user("u1")
    _mk_user("u2", banned=True)
    users_url = reverse("admin_panel:stats-users")
    posts_url = reverse("admin_panel:stats-posts")
    activity_url = reverse("admin_panel:stats-activity")

    resp_users = admin_client.get(users_url)
    resp_posts = admin_client.get(posts_url)
    resp_activity = admin_client.get(activity_url)

    for resp in (resp_users, resp_posts, resp_activity):
        assert resp.status_code == status.HTTP_200_OK
        body = resp.json()
        assert "meta" in body
        assert "data" in body


@pytest.mark.django_db
def test_admin_can_remove_post_and_comment(admin_client):
    author = _mk_user("author")
    post = Post.objects.create(user=author, title="Title", content="Body")
    comment = Comment.objects.create(user=author, post=post, content="c")

    post_url = reverse("admin_panel:remove-post", args=[post.post_id])
    comment_url = reverse("admin_panel:remove-comment", args=[comment.comment_id])

    resp_comment = admin_client.delete(comment_url)
    assert resp_comment.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.filter(comment_id=comment.comment_id).count() == 0

    resp_post = admin_client.delete(post_url)
    assert resp_post.status_code == status.HTTP_204_NO_CONTENT
    assert Post.objects.filter(post_id=post.post_id).count() == 0

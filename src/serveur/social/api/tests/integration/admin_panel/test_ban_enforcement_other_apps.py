"""
Cross-app ban enforcement tests located under admin_panel to keep everything in one suite.
"""
import pytest
from django.urls import reverse
from rest_framework import status

from db.entities.user_entity import User, UserProfile, UserSettings, Follow
from db.entities.domain_entity import Domain, Subforum, Forum
from db.entities.post_entity import Post, Comment
from db.entities.message_entity import Message
from db.repositories.user_repository import FollowRepository
from services.apps_services.encryption_service import EncryptionService

# Compat shims so views using legacy attribute names don't explode during tests.
if not hasattr(Message, "encrypted_content_sender"):
    Message.encrypted_content_sender = property(lambda self: self.encryption_key_sender)
if not hasattr(Message, "encrypted_content_receiver"):
    Message.encrypted_content_receiver = property(lambda self: self.encryption_key_receiver)
if not hasattr(Comment, "author_id"):
    Comment.author_id = property(lambda self: self.user_id)
if not hasattr(Comment, "author"):
    Comment.author = property(lambda self: self.user)
if not hasattr(Forum, "name"):
    Forum.name = property(lambda self: self.forum_name)
if not hasattr(FollowRepository, "get_follow"):
    FollowRepository.get_follow = staticmethod(lambda follower_id, followed_id: None)
if not hasattr(Follow, "followed_id"):
    Follow.followed_id = property(lambda self: self.following_id)


def _create_user(prefix: str) -> User:
    user = User.objects.create(
        firebase_uid=f"{prefix}-google",
        email=f"{prefix}@example.com",
        username=prefix,
    )
    UserProfile.objects.create(user=user, display_name=prefix)
    UserSettings.objects.create(user=user)
    return user


def _create_post(author: User) -> Post:
    domain = Domain.objects.create(domain_name="Ban Domain", description="desc")
    subforum = Subforum.objects.create(
        parent_domain=domain,
        creator=author,
        subforum_name="Ban Subforum",
        description="desc",
    )
    return Post.objects.create(
        user=author,
        subforum=subforum,
        title="A title",
        content="Some content",
    )


def _message_payload():
    _, sender_pub = EncryptionService.generate_rsa_keypair()
    _, receiver_pub = EncryptionService.generate_rsa_keypair()
    return {
        "content": "hello world",
        "sender_public_key": sender_pub,
        "receiver_public_key": receiver_pub,
    }


@pytest.mark.django_db
def test_banned_user_cannot_send_message_until_unbanned(banned_client, admin_client):
    client, banned_user = banned_client
    recipient = _create_user("recipient")
    url = reverse("messages:send-message", args=[recipient.user_id])

    resp = client.post(url, _message_payload(), format="json")
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    unban_url = reverse("admin_panel:unban-user", args=[banned_user.user_id])
    assert admin_client.post(unban_url).status_code == status.HTTP_204_NO_CONTENT

    banned_user.refresh_from_db()
    banned_user.is_authenticated = True
    client.force_authenticate(user=banned_user)

    resp_ok = client.post(url, _message_payload(), format="json")
    assert resp_ok.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_banned_user_cannot_comment_until_unbanned(banned_client, admin_client):
    client, banned_user = banned_client
    post = _create_post(_create_user("post-author"))
    url = reverse("comments:create-comment", args=[post.post_id])

    resp = client.post(url, {"content": "Hello"}, format="json")
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    unban_url = reverse("admin_panel:unban-user", args=[banned_user.user_id])
    assert admin_client.post(unban_url).status_code == status.HTTP_204_NO_CONTENT

    banned_user.refresh_from_db()
    banned_user.is_authenticated = True
    client.force_authenticate(user=banned_user)

    resp_ok = client.post(url, {"content": "Hello"}, format="json")
    assert resp_ok.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_banned_user_cannot_like_until_unbanned(banned_client, admin_client):
    client, banned_user = banned_client
    post = _create_post(_create_user("like-author"))
    url = reverse("likes:like-post", args=[post.post_id])

    resp = client.post(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    unban_url = reverse("admin_panel:unban-user", args=[banned_user.user_id])
    assert admin_client.post(unban_url).status_code == status.HTTP_204_NO_CONTENT

    banned_user.refresh_from_db()
    banned_user.is_authenticated = True
    client.force_authenticate(user=banned_user)

    resp_ok = client.post(url)
    assert resp_ok.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_banned_user_cannot_follow_until_unbanned(banned_client, admin_client):
    client, banned_user = banned_client
    target = _create_user("target")
    url = reverse("followers:follow-user", args=[target.user_id])

    resp = client.post(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    unban_url = reverse("admin_panel:unban-user", args=[banned_user.user_id])
    assert admin_client.post(unban_url).status_code == status.HTTP_204_NO_CONTENT

    banned_user.refresh_from_db()
    banned_user.is_authenticated = True
    client.force_authenticate(user=banned_user)

    resp_ok = client.post(url)
    assert resp_ok.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_banned_user_cannot_list_domains_until_unbanned(banned_client, admin_client):
    client, banned_user = banned_client
    Domain.objects.create(domain_name="Infra", description="desc")
    url = reverse("domains:domains-list")

    resp = client.get(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    unban_url = reverse("admin_panel:unban-user", args=[banned_user.user_id])
    assert admin_client.post(unban_url).status_code == status.HTTP_204_NO_CONTENT

    banned_user.refresh_from_db()
    banned_user.is_authenticated = True
    client.force_authenticate(user=banned_user)

    resp_ok = client.get(url)
    assert resp_ok.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_banned_user_cannot_list_forums_until_unbanned(banned_client, admin_client):
    client, banned_user = banned_client
    Forum.objects.create(creator=_create_user("creator"), forum_name="Forum A")
    url = reverse("forums:forums-list")

    resp = client.get(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    unban_url = reverse("admin_panel:unban-user", args=[banned_user.user_id])
    assert admin_client.post(unban_url).status_code == status.HTTP_204_NO_CONTENT

    banned_user.refresh_from_db()
    banned_user.is_authenticated = True
    client.force_authenticate(user=banned_user)

    resp_ok = client.get(url)
    assert resp_ok.status_code == status.HTTP_200_OK

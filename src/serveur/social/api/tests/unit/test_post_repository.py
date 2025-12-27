import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.exceptions import PermissionDenied
from common.exceptions import NotFoundError, PermissionDeniedError, ConflictError
from apps.posts.views import CreatePostView
from apps.posts.views import PostDetailView
from apps.posts.views import DeletePostView
from apps.posts.views import LikePostView
from apps.posts.views import UnlikePostView
from apps.posts.views import PostLikesView
from apps.posts.views import FeedView
from apps.posts.views import DiscoverView
from db.entities.domain_entity import Forum
from services.apps_services.post_service import PostService

from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime
import uuid
from django.db import models
from django.core.validators import RegexValidator
from db.entities.post_entity import Post, Like
from db.repositories.user_repository import UserRepository
from db.repositories.post_repository import PostRepository
from db.entities.user_entity import User,UserProfile, UserSettings
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError, ConflictError
from db.repositories.domain_repository import DomainRepository, ForumRepository, SubforumRepository

@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = UserRepository.create(
        firebase_id='test-firebase-uid',
        email='test@example.com',
        username='testuser'
    )
    return user

@pytest.fixture
def user2(db):
    """Create a second test user."""
    user = UserRepository.create(
        firebase_id='user2-firebase-uid',
        email='user2@example.com',
        username='user2'
    )
    return user



@pytest.fixture
def test_post(db, test_user):
    """Create a test post."""
    return Post.objects.create(
        user=test_user,
        title='Test Post',
        content='Test content for post'
    )
@pytest.fixture
def test_domain(db, test_user):
    return DomainRepository.create("test domain", "test domain description")


@pytest.fixture
def test_subforum(db, test_user, test_domain):
    return SubforumRepository.create(
        creator_id=test_user.user_id,
        subforum_name="test subforum",
        description="test subforum description",
        parent_domain_id=test_domain.domain_id
    )

@pytest.mark.django_db
class TestPostRepository:

    def test_create_post_success(self, test_user):
        post = PostRepository.create(test_user.user_id, "test post creation","hello world")
        assert post is not None
        assert post.post_id is not None
        assert post.comment_count == 0
        assert post.like_count == 0
        assert post.subforum is None
        assert post.content_signature is None
        assert post.user.user_id == test_user.user_id
        assert post.title == "test post creation"


    def test_create_post_with_subforum_and_signature(self,test_user,test_domain,test_subforum):
        signature = str(uuid.uuid4())
        post = PostRepository.create(test_user.user_id, "test post creation", "hello world",subforum_id=test_subforum.subforum_id, content_signature=signature)
        assert post is not None
        assert post.post_id is not None
        assert post.comment_count == 0
        assert post.like_count == 0
        assert post.user.user_id == test_user.user_id
        assert post.title == "test post creation"
        assert post.subforum == test_subforum
        assert post.content_signature == signature

    def test_get_by_id(self,test_post):
        post = PostRepository.get_by_id(test_post.post_id)
        assert post is not None
        assert post.post_id == test_post.post_id
        assert post.comment_count == 0
        assert post.like_count == 0
        assert post.subforum is None
        assert post.user == test_post.user

    def test_get_none(self):
        post = PostRepository.get_by_id(str(uuid.uuid4()))
        assert post is None

    def test_delete(self,test_user):
        post = PostRepository.create(test_user.user_id, "test post deletion", "hello world")
        deletion = PostRepository.delete(post.post_id)
        assert deletion is True
        get = PostRepository.get_by_id(post.post_id)
        assert get is None

    def test_delete_none(self,test_user):
        deletion = PostRepository.delete(str(uuid.uuid4()))
        assert deletion is False

    def test_feed(self,test_user,test_domain,test_subforum, test_post):
        feed = PostRepository.get_feed(test_user.user_id)
        assert len(feed) == 1
        assert feed[0].post_id == test_post.post_id
        assert feed[0].user.user_id == test_user.user_id

    def test_discover(self,test_user,test_domain,test_subforum, test_post):
        discover = PostRepository.get_discover()
        assert len(discover) == 1
        assert discover[0].post_id == test_post.post_id
        assert discover[0].user.user_id == test_user.user_id

    def test_get_by_subforum(self,test_post,test_user,test_subforum):
        post = PostRepository.create(test_user.user_id, "test post subforum creation","hello world",subforum_id=test_subforum.subforum_id)
        bysubforum = PostRepository.get_by_subforum(test_subforum.subforum_id)
        assert len(bysubforum) == 1
        assert bysubforum[0].post_id == post.post_id
        assert bysubforum[0].user.user_id == test_user.user_id

    def test_increment_and_decrement_likes(self, test_post):
        count = PostRepository.get_by_id(test_post.post_id).like_count
        PostRepository.increment_like_count(test_post.post_id)
        assert PostRepository.get_by_id(test_post.post_id).like_count == count + 1
        PostRepository.decrement_like_count(test_post.post_id)
        assert PostRepository.get_by_id(test_post.post_id).like_count == count


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
from db.entities.post_entity import Post, Like, Comment
from db.entities.user_entity import User

from db.repositories.user_repository import UserRepository
from db.repositories.post_repository import PostRepository, CommentRepository
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
def test_comment(db, test_user, test_post):

    return CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world")


@pytest.mark.django_db
class TestCommentRepository:
      def test_comment_create(self,test_user,test_post):
          nbcomment =   PostRepository.get_by_id(test_post.post_id).comment_count
          """Create a test comment."""
          comment = CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world",parent_comment_id=None)
          assert comment is not None
          assert comment.comment_id is not None
          assert comment.post.post_id == test_post.post_id
          assert comment.user.user_id == test_user.user_id
          assert PostRepository.get_by_id(test_post.post_id).comment_count == nbcomment+1

      def test_reply_comment_create(self,test_user,test_post, test_comment):
          nbcomment = PostRepository.get_by_id(test_post.post_id).comment_count
          comment = CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world",parent_comment_id=test_comment.comment_id)
          assert comment is not None
          assert comment.comment_id is not None
          assert comment.post.post_id == test_post.post_id
          assert comment.user.user_id == test_user.user_id
          assert comment.parent_comment.comment_id == test_comment.comment_id
          assert PostRepository.get_by_id(test_post.post_id).comment_count == nbcomment+1

      def test_get_by_id(self,test_comment):
          comment = CommentRepository.get_by_id(test_comment.comment_id)
          assert comment is not None
          assert comment.comment_id == test_comment.comment_id

      def test_get_None(self):
          comment = CommentRepository.get_by_id(str(uuid.uuid4()))
          assert comment is None

      def test_delete(self,test_user,test_post):
          nbcomment = PostRepository.get_by_id(test_post.post_id).comment_count
          comment = CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world",parent_comment_id=None)
          delete = CommentRepository.delete(comment.comment_id)
          assert delete == True
          assert CommentRepository.get_by_id(comment.comment_id) is None
          assert PostRepository.get_by_id(test_post.post_id).comment_count == nbcomment

      def test_delete_nothing(self):
          delete = CommentRepository.delete(str(uuid.uuid4()))
          assert delete == False

      def test_delete_cascade(self,test_user,test_post):
          nbcomment = PostRepository.get_by_id(test_post.post_id).comment_count
          comment = CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world",parent_comment_id=None)
          reply = CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world",parent_comment_id=comment.comment_id)
          delete = CommentRepository.delete(comment.comment_id)
          assert delete == True
          assert CommentRepository.get_by_id(comment.comment_id) is None
          assert CommentRepository.get_by_id(reply.comment_id) is None
          assert nbcomment == PostRepository.get_by_id(test_post.post_id).comment_count

      def test_get_comment_by_post(self,test_post,test_user,test_comment):
          comment = CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world",parent_comment_id=None)
          comments = CommentRepository.get_by_post(test_post.post_id)
          assert comments is not None
          assert len(comments) == PostRepository.get_by_id(test_post.post_id).comment_count
          assert comments[0].comment_id == comment.comment_id
          assert comments[1].comment_id == test_comment.comment_id

      def test_get_comment_from_non_post(self):
          comments = CommentRepository.get_by_post(str(uuid.uuid4()))
          assert comments is None or len(comments) == 0

      def test_get_replies(self,test_comment,test_user,test_post):
          reply = CommentRepository.create(test_user.user_id,test_post.post_id,"Hello world",parent_comment_id=test_comment.comment_id)
          replies = CommentRepository.get_replies(test_comment.comment_id)
          assert replies is not None
          assert len(replies) == 1
          assert replies[0].comment_id == reply.comment_id

      def test_get_replies_from_non_comment(self):
          replies = CommentRepository.get_replies(str(uuid.uuid4()))
          assert replies is None or len(replies) == 0
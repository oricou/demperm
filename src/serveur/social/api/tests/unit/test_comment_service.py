import time
import uuid
from multiprocessing.connection import wait

import pytest
import unittest
from unittest import mock
from rest_framework import status
from datetime import datetime

from rest_framework.exceptions import NotFound

from services.apps_services.post_service import PostService
from services.apps_services.comment_service import CommentService
from services.apps_services.user_service import UserService
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError
from db.entities.post_entity import Comment
from rest_framework import status
from db.repositories.user_repository import UserRepository, BlockRepository, FollowRepository
from db.repositories.post_repository import PostRepository, CommentRepository
from db.repositories.domain_repository import SubforumRepository
from db.entities.domain_entity import Forum, Subforum


"""def create_mock_comment(comment_id, post_id, user_id, content, parent_comment_id=None):
    comment = mock.Mock(spec=Comment)
    comment.comment_id = comment_id
    comment.post_id = post_id
    comment.user_id = user_id
    comment.content = content
    comment.parent_comment_id = parent_comment_id
    comment.created_at = datetime.now()
    comment.updated_at = datetime.now()
    return comment


def create_mock_user(user_id, is_admin=False):
    user = mock.Mock()
    user.user_id = user_id
    user.is_admin = is_admin
    return user


@mock.patch('db.repositories.message_repository.AuditLogRepository')
@mock.patch('db.repositories.post_repository.PostRepository')
@mock.patch('db.repositories.post_repository.CommentRepository')
@mock.patch('db.repositories.user_repository.UserRepository')
@mock.patch('common.validators.Validator')"""

@pytest.fixture
def user(db):
    """Create a test user."""
    return UserRepository.create(
        firebase_id=str(uuid.uuid4()),
        email="user@gmail.com",
        username="alice",
    )

@pytest.fixture
def viewer(db):
    """Create a viewer user."""
    return UserRepository.create(
        firebase_id=str(uuid.uuid4()),
        email="viewer@gmail.com",
        username="bob",
    )

@pytest.fixture
def blocked(db):
    """Create a blocked user."""
    return UserRepository.create(
        firebase_id=str(uuid.uuid4()),
        email="hank@gmail.com",
        username="hank",
    )

@pytest.fixture
def block(db, user, blocked):
    """Create a block relationship."""
    return BlockRepository.create(
        blocker_id=user.user_id,
        blocked_id=blocked.user_id,
    )

@pytest.fixture
def forum(db, user):
    """Create a forum."""
    return Forum.objects.create(creator=user, forum_name='TestForum', description='d')

@pytest.fixture
def subforum(db, user, forum):
    """Create a subforum."""
    return SubforumRepository.create(
        creator_id=user.user_id,
        subforum_name="General Discussion",
        description="Test subforum",
        parent_forum_id=forum.forum_id,
    )

@pytest.fixture
def post(db, user, subforum):
    """Create a post."""
    return PostRepository.create(
        user_id=user.user_id,
        subforum_id=subforum.subforum_id,
        title="Test Post",
        content="Hello world",
    )

@pytest.fixture
def post2(db, viewer, subforum):
    """Create a second post."""
    return PostRepository.create(
        user_id=viewer.user_id,
        subforum_id=subforum.subforum_id,
        title="Test Post",
        content="Hello world",
    )

@pytest.fixture
def private(db):
    """Create a private user."""
    user = UserRepository.create(
        firebase_id=str(uuid.uuid4()),
        email="patrick@gmail.com",
        username="patrick",
    )
    updates = {"privacy": "private"}
    UserService.update_user_profile(user.user_id, **updates)
    return user

@pytest.fixture
def privpost(db, private, subforum):
    """Create a post from private user."""
    return PostRepository.create(
        user_id=private.user_id,
        subforum_id=subforum.subforum_id,
        title="Happy anniversary NIcole",
        content="Happy anniversary NIcole",
    )

@pytest.fixture
def follow(db, viewer, private):
    """Create a follow relationship."""
    return FollowRepository.create(follower_id=viewer.user_id, following_id=private.user_id)

@pytest.fixture
def comment(db, user, post):
    """Create a comment."""
    return CommentRepository.create(user.user_id, post.post_id, "Nice", None)

@pytest.fixture
def service():
    """Create comment service instance."""
    return CommentService()

@pytest.mark.django_db
class TestCommentService:

    def test_get_comment_by_id(self, service, comment, user, post):
        one_comment = service.get_comment_by_id(comment.comment_id)
        assert one_comment.comment_id == comment.comment_id
        assert one_comment.user.user_id == user.user_id
        assert one_comment.post.post_id == post.post_id

    def test_get_comment_by_non_id(self, service):
        with pytest.raises(NotFoundError):
            service.get_comment_by_id(str(uuid.uuid4()))


    def test_create_comment(self, service, viewer, post):
        precount = PostService.get_post_by_id(post.post_id).comment_count+1
        new_comment = service.create_comment(viewer.user_id, post.post_id, "Meh", None)
        assert new_comment.user.user_id == viewer.user_id
        assert new_comment.post.post_id == post.post_id
        assert new_comment.content == "Meh"
        assert PostService.get_post_by_id(post.post_id).comment_count == precount

    def test_create_comment_non_post(self, service, viewer):
        with pytest.raises(NotFoundError):
            service.create_comment(viewer.user_id, str(uuid.uuid4()), "Nice", None)

    def test_comment_as_blocked(self, service, blocked, post, block):
        with pytest.raises(PermissionDeniedError):
            service.create_comment(blocked.user_id, post.post_id, "I hate you ALice", None)

    def test_comment_private_no_follow(self, service, user, privpost):
        with pytest.raises(PermissionDeniedError):
            service.create_comment(user.user_id, privpost.post_id, "Meh", None)

    def test_comment_private_follow(self, service, viewer, privpost, follow):
        commentcount = PostService.get_post_by_id(privpost.post_id).comment_count+1
        new_comment = service.create_comment(viewer.user_id, privpost.post_id, "Meh", None)
        assert new_comment.user.user_id == viewer.user_id
        assert new_comment.post.post_id == privpost.post_id
        assert new_comment.content == "Meh"
        assert PostService.get_post_by_id(privpost.post_id).comment_count == commentcount

    def test_get_one_from_post(self, service, post, comment):
        single = service.get_post_comments(post.post_id)
        assert len(single) == 1
        assert single[0].comment_id == comment.comment_id
        assert single[0].post.post_id == post.post_id

    def test_get_no_comment_from_post(self, service, post2):
        zero = service.get_post_comments(post2.post_id)
        assert len(zero) == 0

    def test_get_comment_from_no_post(self, service):
        with pytest.raises(NotFoundError):
            service.get_post_comments(str(uuid.uuid4()))

    def test_get_multiple_comments(self, service, viewer, private, post, comment, user):
        second = service.create_comment(viewer.user_id, post.post_id, "Meh", None)
        time.sleep(4)
        third = service.create_comment(private.user_id, post.post_id, "cool", None)
        three = service.get_post_comments(post.post_id)
        assert len(three) == 3
        assert three[2].comment_id == comment.comment_id
        assert three[2].post.post_id == post.post_id
        assert three[2].user.user_id == user.user_id
        assert three[1].comment_id == second.comment_id
        assert three[1].post.post_id == post.post_id
        assert three[1].user.user_id == viewer.user_id
        assert three[0].comment_id == third.comment_id
        assert three[0].post.post_id == post.post_id
        assert three[0].user.user_id == private.user_id

    def test_make_reply(self, service, viewer, post, comment):
        nb_comment = PostService.get_post_by_id(post.post_id).comment_count+1
        reply = service.create_comment(viewer.user_id, post.post_id, "Noice", comment.comment_id)
        assert reply.user.user_id == viewer.user_id
        assert reply.post.post_id == post.post_id
        assert reply.content == "Noice"
        assert reply.parent_comment.comment_id == comment.comment_id
        assert nb_comment == PostService.get_post_by_id(post.post_id).comment_count

    def test_make_reply_to_no_post(self, service, viewer, comment):
        with pytest.raises(NotFoundError):
            service.create_comment(viewer.user_id, str(uuid.uuid4()), "Meh", comment.comment_id)

    def test_make_reply_to_non_comment(self, service, viewer, post):
        with pytest.raises(NotFoundError):
            service.create_comment(viewer.user_id, post.post_id, "Meh", str(uuid.uuid4()))

    def test_make_reply_to_comment_from_wrong_post(self, service, viewer, post2, comment):
        with pytest.raises(ValidationError):
            service.create_comment(viewer.user_id, post2.post_id, "Meh", comment.comment_id)

    def test_reply_while_blocked(self, service, blocked, post, post2, user, comment, block):
        with pytest.raises(PermissionDeniedError):
            service.create_comment(blocked.user_id, post.post_id, "Meh", comment.comment_id)

        comment2 = service.create_comment(user.user_id, post2.post_id, "Meh", None)
        with pytest.raises(PermissionDeniedError):
            service.create_comment(blocked.user_id, post2.post_id, "Meh", comment2.comment_id)

    def test_reply_private_follow(self, service, viewer, privpost, follow):
        new_comment = service.create_comment(viewer.user_id, privpost.post_id, "Meh", None)
        nb_comment = PostService.get_post_by_id(privpost.post_id).comment_count+1

        new_reply = service.create_comment(viewer.user_id, privpost.post_id, "Meh", new_comment.comment_id)
        assert new_reply.user.user_id == viewer.user_id
        assert new_reply.post.post_id == privpost.post_id
        assert new_reply.parent_comment.comment_id == new_comment.comment_id
        assert nb_comment == PostService.get_post_by_id(privpost.post_id).comment_count

    def test_reply_private_no_follow(self, service, viewer, user, privpost, follow):
        private_reply = service.create_comment(viewer.user_id, privpost.post_id, "Meh", None)
        with pytest.raises(PermissionDeniedError):
            service.create_comment(user.user_id, privpost.post_id, "Meh", private_reply.comment_id)

    def test_delete_comment(self, service, user, post):
        nb_comment = PostService.get_post_by_id(post.post_id).comment_count
        todel = service.create_comment(user.user_id, post.post_id, "Meh", None)
        service.delete_comment(todel.comment_id, user.user_id)
        assert nb_comment == PostService.get_post_by_id(post.post_id).comment_count
        with pytest.raises(NotFoundError):
            service.get_comment_by_id(todel.comment_id)

    def test_delete_no_post(self, service, user):
        with pytest.raises(NotFoundError):
            service.delete_comment(str(uuid.uuid4()), user.user_id)

    def test_delete_wrong_user(self, service, comment):
        with pytest.raises(NotFoundError):
            service.delete_comment(comment.comment_id, str(uuid.uuid4()))

    def test_delete_replies(self, service, user, post, comment):
        nbcomment = PostService.get_post_by_id(post.post_id).comment_count
        reply = service.create_comment(user.user_id, post.post_id, "Meh", comment.comment_id)
        service.delete_comment(reply.comment_id, user.user_id)
        assert nbcomment == PostService.get_post_by_id(post.post_id).comment_count
        with pytest.raises(NotFoundError):
            service.get_comment_by_id(reply.comment_id)

    def test_delete_cascade(self, service, user, post):
        nb_comment = PostService.get_post_by_id(post.post_id).comment_count
        todel = service.create_comment(user.user_id, post.post_id, "Meh", None)
        tocascade = service.create_comment(user.user_id, post.post_id, "Meh", todel.comment_id)

        service.delete_comment(todel.comment_id, user.user_id)
        assert nb_comment == PostService.get_post_by_id(post.post_id).comment_count
        with pytest.raises(NotFoundError):
            service.get_comment_by_id(todel.comment_id)
        with pytest.raises(NotFoundError):
            service.get_comment_by_id(tocascade.comment_id)


    


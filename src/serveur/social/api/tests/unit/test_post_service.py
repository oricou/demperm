import unittest

import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from services.apps_services.post_service import PostService
from common.exceptions import NotFoundError,ConflictError, ValidationError, PermissionDeniedError
from db.repositories.post_repository import PostRepository
from django.db import models
from uuid import uuid4
from rest_framework import status
from db.entities.domain_entity import Subforum, Domain, Forum
from db.entities.user_entity import User
from db.entities.post_entity import Post, Like
from db.repositories.post_repository import PostRepository, CommentRepository
from db.repositories.user_repository import UserRepository, BlockRepository, FollowRepository
from db.repositories.domain_repository import SubforumRepository
from services.apps_services.user_service import UserService

class PostServiceTest(unittest.TestCase):

    def setUp(self):
        # Create users
        # Create user
        self.user = UserRepository.create(
            firebase_uid=str(uuid.uuid4()),
            email="user@gmail.com",
            username="alice",

        )

        # Create viewer user (for permission tests)
        self.viewer = UserRepository.create(
            firebase_uid=str(uuid.uuid4()),
            email="viewer@gmail.com",
            username="bob",
        )

        self.blocked = UserRepository.create(
            firebase_uid=str(uuid.uuid4()),
            email="hank@gmail.com",
            username="hank",
        )

        self.block = BlockRepository.create(
            blocker_id=self.user.user_id,
            blocked_id=self.blocked.user_id,
        )

        self.private = UserRepository.create(
            firebase_id=str(uuid.uuid4()),
            email="patrick@gmail.com",
            username="patrick",
        )
        updates = {"privacy": False}

        UserService.update_user_profile(self.private.user_id,**updates)

        self.admin = UserRepository.create(
            firebase_id=str(uuid.uuid4()),
            email="admin@gmail.com",
            username = "admin",
        )
        self.admin.is_admin = True
        self.admin.save()
        
        #self.domain = Domain.objects.create(domain_name='TestDomain', description='d')
        self.forum = Forum.objects.create(creator=self.user, forum_name='TestForum', description='d')
        # Create a valid subforum
        self.subforum = SubforumRepository.create(
            creator_id=self.user.user_id,
            subforum_name="General Discussion",
            description="Test subforum",

            parent_forum_id=self.forum.forum_id,
        )

        # Create posts inside that subforum
        self.post = PostRepository.create(
            user_id=self.user.user_id,
            subforum_id=self.subforum.subforum_id,
            title="Test Post",
            content="Hello world",

        )

        self.post_to_del = PostRepository.create(
            user_id=self.user.user_id,
            subforum_id=self.subforum.subforum_id,
            title="to del",
            content="to del",
        )
        self.post2 = PostRepository.create(
            user_id=self.viewer.user_id,
            subforum_id=self.subforum.subforum_id,
            title="Test Post",
            content="Hello world",

        )
        self.post_to_del2 = PostRepository.create(
            user_id=self.viewer.user_id,
            subforum_id=self.subforum.subforum_id,
            title="to del",
            content="to del",
        )

        self.privpost = PostRepository.create(
            user_id=self.private.user_id,
            subforum_id=self.subforum.subforum_id,
            title = "Happy anniversary NIcole",
            content= "Happy anniversary NIcole",
        )

        self.blockpost = PostRepository.create(
            user_id=self.blocked.user_id,
            subforum_id=self.subforum.subforum_id,
            title = "I hate Alice",
            content= "I HATE ALICE!!!!!!!!! >:("
        )

        self.follow= FollowRepository.create(follower_id=self.viewer.user_id, following_id=self.private.user_id)


        self.service = PostService()

        # ----------------------------------------------------------------------
        # TEST: get_post
        # ----------------------------------------------------------------------
    def test_get_post_as_owner(self):
        post = self.service.get_post_by_id(post_id=self.post.post_id)
        assert post.post_id == self.post.post_id

    def test_get_post_as_viewer(self):
            post = self.service.get_post_by_id(viewer_id=self.viewer.user_id, post_id=self.post.post_id)
            assert post.post_id == self.post.post_id

    def test_get_post_missing_raises_exception(self):
        with pytest.raises(NotFoundError):
            self.service.get_post_by_id(post_id=str(uuid.uuid4()))

    def test_get_post_as_blocked(self):
        with ((pytest.raises(PermissionDeniedError))):
            self.service.get_post_by_id(viewer_id=self.blocked.user_id,post_id=self.post.post_id)

    def test_get_post_as_blocker(self):
        with ((pytest.raises(PermissionDeniedError))):
            self.service.get_post_by_id(viewer_id=self.user.user_id,post_id=self.blockpost.post_id)

    def test_get_post_private_no_follow(self):
        with ((pytest.raises(PermissionDeniedError))):
            self.service.get_post_by_id(viewer_id=self.user.user_id,post_id=self.privpost.post_id)


    def test_get_post_private_with_follow(self):
        post = self.service.get_post_by_id(viewer_id=self.viewer.user_id,post_id=self.privpost.post_id)
        assert post.post_id == self.privpost.post_id
        assert post.user.user_id == self.private.user_id
    #def test_get_post_as_blocked(self):

        # ----------------------------------------------------------------------
        # TEST: delete_post
        # ----------------------------------------------------------------------
    def test_delete_post_by_owner(self):
        self.service.delete_post(user_id=self.user.user_id, post_id=self.post_to_del.post_id)
        assert not Post.objects.filter(post_id=self.post_to_del.post_id).exists()

    def test_delete_post_by_stranger_raises(self):
        with pytest.raises(PermissionDeniedError):
            self.service.delete_post(user_id=self.user.user_id, post_id=self.post_to_del2.post_id)


    def test_delete_as_admin(self):
        self.service.delete_post(user_id=self.admin.user_id, post_id=self.post_to_del2.post_id)
        assert not Post.objects.filter(post_id=self.post_to_del2.post_id).exists()
        # ----------------------------------------------------------------------
        # TEST: create_post
        # ----------------------------------------------------------------------
    def test_create_post(self):
        new_post = self.service.create_post(
            user_id=self.viewer.user_id,
            title="viewer's post",
            subforum_id=self.subforum.subforum_id,
            content="My first post!"
        )
        assert new_post.user == self.viewer
        assert new_post.content == "My first post!"
        assert new_post.subforum == self.subforum

    def test_create_post_invalid_subforum(self):
        with ((pytest.raises(NotFoundError))):
            self.service.create_post(
                user_id=self.viewer.user_id,subforum_id=str(uuid.uuid4()),title="whatever",content="Hi")

    def test_like_post(self):
        pre_like_count = self.post2.like_count+1
        like = self.service.like_post(post_id=self.post2.post_id, user_id=self.viewer.user_id)
        assert like.user.user_id == self.viewer.user_id
        assert like.post.post_id == self.post2.post_id
        assert pre_like_count == self.service.get_post_by_id(self.post2.post_id).like_count

    def test_like_post_has_blocked(self):
        with ((pytest.raises(PermissionDeniedError))):
            self.service.like_post(post_id=self.post.post_id, user_id=self.blocked.user_id)

    def test_like_post_has_blocker(self):
        with ((pytest.raises(PermissionDeniedError))):
            self.service.like_post(post_id=self.blockpost.post_id, user_id=self.user.user_id)

    def test_like_not_followed(self):
        with ((pytest.raises(PermissionDeniedError))):
            self.service.like_post(post_id=self.privpost.post_id, user_id=self.user.user_id)

    def test_like_follow_post(self):
        pre_like_count = self.service.get_post_by_id(self.privpost.post_id).like_count+1
        like = self.service.like_post(post_id=self.privpost.post_id, user_id=self.viewer.user_id)
        assert like.user.user_id == self.viewer.user_id
        assert like.post.post_id == self.privpost.post_id
        assert pre_like_count == self.service.get_post_by_id(self.privpost.post_id).like_count

    def test_unlike_post(self):
        self.service.like_post(post_id=self.post2.post_id, user_id=self.viewer.user_id)
        pre_like_count = self.service.get_post_by_id(self.post2.post_id).like_count-1
        self.service.unlike_post(post_id=self.post2.post_id, user_id=self.viewer.user_id)

        assert pre_like_count == self.service.get_post_by_id(self.post2.post_id).like_count

    def test_like_not_existing_post(self):
        with (pytest.raises(NotFoundError)):
            self.service.like_post(post_id=str(uuid.uuid4()), user_id=self.viewer.user_id)

    def test_like_twice(self):
        self.service.like_post(post_id=self.post2.post_id, user_id=self.viewer.user_id)
        with (pytest.raises(ConflictError)):
            self.service.like_post(post_id=self.post2.post_id, user_id=self.viewer.user_id)
    def test_unlike_no_liked_post(self):
        with(pytest.raises(NotFoundError)):
            self.service.unlike_post(post_id=self.post2.post_id, user_id=self.viewer.user_id)

    def test_get_no_likers(self):
        list_likes = self.service.get_post_likes(self.post2.post_id)
        assert len(list_likes) == 0

    def test_get_likers(self):
        like = self.service.like_post(post_id=self.post2.post_id, user_id=self.viewer.user_id)
        list_likes = self.service.get_post_likes(self.post2.post_id)
        assert list_likes[0].like_id == like.like_id
        assert list_likes[0].post.post_id == self.post2.post_id
        assert list_likes[0].user.user_id == self.viewer.user_id

    def test_get_like_from_no_post(self):
        with(pytest.raises(NotFoundError)):
            self.service.get_post_likes(str(uuid.uuid4()))

    def test_feed(self):
        feed = self.service.get_feed(self.viewer.user_id)
        assert len(feed) == 6

    def test_discover(self):
        self.service.like_post(post_id=self.post.post_id, user_id=self.viewer.user_id)
        self.service.like_post(post_id=self.post.post_id, user_id=self.private.user_id)
        self.service.like_post(post_id=self.post2.post_id, user_id=self.user.user_id)
        discover = self.service.get_discover()
        assert len(discover) == 6
        assert discover[0].post_id == self.post.post_id
        assert discover[1].post_id == self.post2.post_id



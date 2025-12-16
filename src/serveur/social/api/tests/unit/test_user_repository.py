"""
Unit tests for User, Block, and Follow repositories.
Tests data access layer with real database.
"""
import pytest
import uuid
from db.repositories.user_repository import UserRepository, BlockRepository, FollowRepository
from db.entities.user_entity import User, UserProfile, UserSettings, Block, Follow


@pytest.fixture
def test_user(db):
    """Create a test user."""
    return UserRepository.create(
        firebase_uid='test-firebase-uid',
        email='test@example.com',
        username='testuser'
    )


@pytest.fixture
def user2(db):
    """Create a second test user."""
    return UserRepository.create(
        firebase_uid='user2-firebase-uid',
        email='user2@example.com',
        username='user2'
    )


@pytest.fixture
def user3(db):
    """Create a third test user."""
    return UserRepository.create(
        firebase_uid='user3-firebase-uid',
        email='user3@example.com',
        username='user3'
    )


@pytest.mark.django_db
class TestUserRepository:
    """Test UserRepository operations."""
    
    def test_get_by_id_success(self, test_user):
        """Test getting user by ID successfully."""
        user = UserRepository.get_by_id(str(test_user.user_id))
        
        assert user is not None
        assert user.user_id == test_user.user_id
        assert user.username == 'testuser'
        # Check that profile and settings are loaded
        assert hasattr(user, 'profile')
        assert hasattr(user, 'settings')
    
    def test_get_by_id_non_existing(self):
        """Test getting non-existing user returns None."""
        fake_id = str(uuid.uuid4())
        
        user = UserRepository.get_by_id(fake_id)
        
        assert user is None
    
    def test_get_by_firebase_uid(self, test_user):
        """Test getting user by Firebase UID."""
        user = UserRepository.get_by_firebase_uid('test-firebase-uid')
        
        assert user is not None
        assert user.firebase_uid == 'test-firebase-uid'
        assert user.username == 'testuser'
    
    def test_get_by_firebase_uid_non_existing(self):
        """Test getting user by non-existing Firebase UID returns None."""
        user = UserRepository.get_by_firebase_uid('non-existing-uid')
        
        assert user is None
    
    def test_get_by_email(self, test_user):
        """Test getting user by email."""
        user = UserRepository.get_by_email('test@example.com')
        
        assert user is not None
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
    
    def test_get_by_email_non_existing(self):
        """Test getting user by non-existing email returns None."""
        user = UserRepository.get_by_email('nonexisting@example.com')
        
        assert user is None
    
    def test_get_by_username(self, test_user):
        """Test getting user by username."""
        user = UserRepository.get_by_username('testuser')
        
        assert user is not None
        assert user.username == 'testuser'
    
    def test_get_by_username_non_existing(self):
        """Test getting user by non-existing username returns None."""
        user = UserRepository.get_by_username('nonexistinguser')
        
        assert user is None
    
    def test_create_user_with_profile_settings(self):
        """Test creating user also creates profile and settings."""
        user = UserRepository.create(
            firebase_uid='new-user-uid',
            email='newuser@example.com',
            username='newuser'
        )
        
        assert user is not None
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.firebase_uid == 'new-user-uid'
        
        # Check profile was created
        profile = UserProfile.objects.filter(user=user).first()
        assert profile is not None
        
        # Check settings were created
        settings = UserSettings.objects.filter(user=user).first()
        assert settings is not None
    
    def test_update_user_fields(self, test_user):
        """Test updating user fields."""
        updated_user = UserRepository.update(
            test_user,
            username='updateduser',
            email='updated@example.com'
        )
        
        assert updated_user.username == 'updateduser'
        assert updated_user.email == 'updated@example.com'
        
        # Verify in database
        user_from_db = UserRepository.get_by_id(str(test_user.user_id))
        assert user_from_db.username == 'updateduser'
    
    def test_search_by_username_case_insensitive(self):
        """Test searching users by username is case-insensitive."""
        UserRepository.create(
            firebase_uid='search-uid-1',
            email='search1@example.com',
            username='SearchUser'
        )
        
        # Search with lowercase
        results = UserRepository.search_by_username('search', page=1, page_size=20)
        
        assert len(results) >= 1
        assert any(u.username == 'SearchUser' for u in results)
    
    def test_search_excludes_banned_users(self):
        """Test search excludes banned users."""
        # Create normal user
        normal_user = UserRepository.create(
            firebase_uid='normal-uid',
            email='normal@example.com',
            username='normaluser'
        )
        
        # Create banned user
        banned_user = UserRepository.create(
            firebase_uid='banned-uid',
            email='banned@example.com',
            username='banneduser'
        )
        banned_user.is_banned = True
        banned_user.save()
        
        # Search should only return normal user
        results = UserRepository.search_by_username('user', page=1, page_size=20)
        usernames = [u.username for u in results]
        
        assert 'normaluser' in usernames
        assert 'banneduser' not in usernames
    
    def test_search_pagination(self):
        """Test search pagination works correctly."""
        # Create multiple users
        for i in range(15):
            UserRepository.create(
                firebase_uid=f'page-uid-{i}',
                email=f'page{i}@example.com',
                username=f'pageuser{i:02d}'
            )
        
        # Get first page
        page1 = UserRepository.search_by_username('pageuser', page=1, page_size=10)
        assert len(page1) == 10
        
        # Get second page
        page2 = UserRepository.search_by_username('pageuser', page=2, page_size=10)
        assert len(page2) == 5
    
    def test_get_bulk_users(self, test_user, user2, user3):
        """Test getting multiple users by IDs."""
        user_ids = [str(test_user.user_id), str(user2.user_id), str(user3.user_id)]
        
        users = UserRepository.get_bulk(user_ids)
        
        assert len(users) == 3
        usernames = [u.username for u in users]
        assert 'testuser' in usernames
        assert 'user2' in usernames
        assert 'user3' in usernames
    
    def test_get_bulk_excludes_banned(self, test_user, user2):
        """Test get_bulk excludes banned users."""
        # Ban user2
        user2.is_banned = True
        user2.save()
        
        user_ids = [str(test_user.user_id), str(user2.user_id)]
        users = UserRepository.get_bulk(user_ids)
        
        # Should only return test_user
        assert len(users) == 1
        assert users[0].username == 'testuser'
    
    def test_username_unique_constraint(self):
        """Test that usernames must be unique."""
        UserRepository.create(
            firebase_uid='unique-uid-1',
            email='unique1@example.com',
            username='uniqueuser'
        )
        
        # Attempting to create user with same username should fail
        with pytest.raises(Exception):  # Django IntegrityError
            UserRepository.create(
                firebase_uid='unique-uid-2',
                email='unique2@example.com',
                username='uniqueuser'
            )
    
    def test_email_unique_constraint(self):
        """Test that emails must be unique."""
        UserRepository.create(
            firebase_uid='email-uid-1',
            email='unique@example.com',
            username='emailuser1'
        )
        
        # Attempting to create user with same email should fail
        with pytest.raises(Exception):  # Django IntegrityError
            UserRepository.create(
                firebase_uid='email-uid-2',
                email='unique@example.com',
                username='emailuser2'
            )
    
    def test_firebase_uid_unique_constraint(self):
        """Test that Firebase UIDs must be unique."""
        UserRepository.create(
            firebase_uid='same-firebase-uid',
            email='firebase1@example.com',
            username='firebaseuser1'
        )
        
        # Attempting to create user with same Firebase UID should fail
        with pytest.raises(Exception):  # Django IntegrityError
            UserRepository.create(
                firebase_uid='same-firebase-uid',
                email='firebase2@example.com',
                username='firebaseuser2'
            )


@pytest.mark.django_db
class TestBlockRepository:
    """Test BlockRepository operations."""
    
    def test_create_block(self, test_user, user2):
        """Test creating a block."""
        block = BlockRepository.create(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        assert block is not None
        assert str(block.blocker_id) == str(test_user.user_id)
        assert str(block.blocked_id) == str(user2.user_id)
    
    def test_delete_block(self, test_user, user2):
        """Test deleting a block."""
        BlockRepository.create(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        result = BlockRepository.delete(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        assert result is True
        assert not BlockRepository.is_blocked(
            str(test_user.user_id),
            str(user2.user_id)
        )
    
    def test_delete_non_existing_block(self, test_user, user2):
        """Test deleting non-existing block returns False."""
        result = BlockRepository.delete(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        assert result is False
    
    def test_is_blocked_true(self, test_user, user2):
        """Test checking if user is blocked returns True."""
        BlockRepository.create(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        is_blocked = BlockRepository.is_blocked(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        assert is_blocked is True
    
    def test_is_blocked_false(self, test_user, user2):
        """Test checking if user is not blocked returns False."""
        is_blocked = BlockRepository.is_blocked(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        assert is_blocked is False
    
    def test_get_blocked_users_pagination(self, test_user, user2, user3):
        """Test getting list of blocked users with pagination."""
        # Block multiple users
        BlockRepository.create(str(test_user.user_id), str(user2.user_id))
        BlockRepository.create(str(test_user.user_id), str(user3.user_id))
        
        blocked = BlockRepository.get_blocked_users(
            blocker_id=str(test_user.user_id),
            page=1,
            page_size=10
        )
        
        assert len(blocked) == 2
    
    def test_get_blocked_users_empty(self, test_user):
        """Test getting blocked users when none are blocked."""
        blocked = BlockRepository.get_blocked_users(
            blocker_id=str(test_user.user_id)
        )
        
        assert len(blocked) == 0
    
    def test_block_unique_constraint(self, test_user, user2):
        """Test that same block cannot be created twice."""
        BlockRepository.create(
            blocker_id=str(test_user.user_id),
            blocked_id=str(user2.user_id)
        )
        
        # Attempting to create duplicate block should fail
        with pytest.raises(Exception):  # Django IntegrityError
            BlockRepository.create(
                blocker_id=str(test_user.user_id),
                blocked_id=str(user2.user_id)
            )


@pytest.mark.django_db
class TestFollowRepository:
    """Test FollowRepository operations."""
    
    def test_create_follow_accepted(self, test_user, user2):
        """Test creating an accepted follow relationship."""
        follow = FollowRepository.create(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id),
            status='accepted'
        )
        
        assert follow is not None
        assert str(follow.follower_id) == str(test_user.user_id)
        assert str(follow.following_id) == str(user2.user_id)
        assert follow.status == 'accepted'
    
    def test_create_follow_pending(self, test_user, user2):
        """Test creating a pending follow request."""
        follow = FollowRepository.create(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id),
            status='pending'
        )
        
        assert follow.status == 'pending'
    
    def test_delete_follow(self, test_user, user2):
        """Test deleting a follow relationship."""
        FollowRepository.create(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id)
        )
        
        result = FollowRepository.delete(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id)
        )
        
        assert result is True
    
    def test_delete_non_existing_follow(self, test_user, user2):
        """Test deleting non-existing follow returns False."""
        result = FollowRepository.delete(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id)
        )
        
        assert result is False
    
    def test_update_status_pending_to_accepted(self, test_user, user2):
        """Test updating follow status from pending to accepted."""
        FollowRepository.create(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id),
            status='pending'
        )
        
        updated_follow = FollowRepository.update_status(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id),
            status='accepted'
        )
        
        assert updated_follow is not None
        assert updated_follow.status == 'accepted'
    
    def test_update_status_non_existing(self, test_user, user2):
        """Test updating status of non-existing follow returns None."""
        result = FollowRepository.update_status(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id),
            status='accepted'
        )
        
        assert result is None
    
    def test_get_followers_pagination(self, test_user, user2, user3):
        """Test getting user's followers with pagination."""
        # user2 and user3 follow test_user
        FollowRepository.create(str(user2.user_id), str(test_user.user_id), 'accepted')
        FollowRepository.create(str(user3.user_id), str(test_user.user_id), 'accepted')
        
        followers = FollowRepository.get_followers(
            user_id=str(test_user.user_id),
            status='accepted',
            page=1,
            page_size=10
        )
        
        assert len(followers) == 2
    
    def test_get_followers_only_accepted(self, test_user, user2, user3):
        """Test get_followers only returns accepted follows."""
        FollowRepository.create(str(user2.user_id), str(test_user.user_id), 'accepted')
        FollowRepository.create(str(user3.user_id), str(test_user.user_id), 'pending')
        
        followers = FollowRepository.get_followers(
            user_id=str(test_user.user_id),
            status='accepted'
        )
        
        assert len(followers) == 1
    
    def test_get_following_pagination(self, test_user, user2, user3):
        """Test getting users that user is following."""
        # test_user follows user2 and user3
        FollowRepository.create(str(test_user.user_id), str(user2.user_id), 'accepted')
        FollowRepository.create(str(test_user.user_id), str(user3.user_id), 'accepted')
        
        following = FollowRepository.get_following(
            user_id=str(test_user.user_id),
            status='accepted',
            page=1,
            page_size=10
        )
        
        assert len(following) == 2
    
    def test_get_pending_requests(self, test_user, user2, user3):
        """Test getting pending follow requests."""
        # user2 and user3 request to follow test_user
        FollowRepository.create(str(user2.user_id), str(test_user.user_id), 'pending')
        FollowRepository.create(str(user3.user_id), str(test_user.user_id), 'pending')
        
        pending = FollowRepository.get_pending_requests(str(test_user.user_id))
        
        assert len(pending) == 2
        assert all(f.status == 'pending' for f in pending)
    
    def test_follow_unique_constraint(self, test_user, user2):
        """Test that same follow relationship cannot be created twice."""
        FollowRepository.create(
            follower_id=str(test_user.user_id),
            following_id=str(user2.user_id)
        )
        
        # Attempting to create duplicate should fail
        with pytest.raises(Exception):  # Django IntegrityError
            FollowRepository.create(
                follower_id=str(test_user.user_id),
                following_id=str(user2.user_id)
            )

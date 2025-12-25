"""
Unit tests for User entity models.
Tests model constraints, defaults, and relationships.
"""
import pytest
from django.db import IntegrityError
from db.entities.user_entity import User, UserProfile, UserSettings, Block, Follow
from db.repositories.user_repository import UserRepository


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""
    
    def test_user_creation_defaults(self):
        """Test user is created with correct default values."""
        user = User.objects.create(
            firebase_uid='test-uid',
            email='test@example.com',
            username='testuser'
        )
        
        assert user.user_id is not None
        assert user.is_admin is False
        assert user.is_banned is False
        assert user.created_at is not None
    
    def test_user_str_representation(self):
        """Test __str__ method returns username."""
        user = User.objects.create(
            firebase_uid='str-uid',
            email='str@example.com',
            username='struser'
        )
        
        assert str(user) == 'struser'
    
    def test_username_unique_constraint(self):
        """Test username must be unique."""
        User.objects.create(
            firebase_uid='uid1',
            email='email1@example.com',
            username='uniqueuser'
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create(
                firebase_uid='uid2',
                email='email2@example.com',
                username='uniqueuser'
            )
    
    def test_email_unique_constraint(self):
        """Test email must be unique."""
        User.objects.create(
            firebase_uid='uid1',
            email='unique@example.com',
            username='user1'
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create(
                firebase_uid='uid2',
                email='unique@example.com',
                username='user2'
            )
    
    def test_firebase_uid_unique_constraint(self):
        """Test Firebase UID must be unique."""
        User.objects.create(
            firebase_uid='unique-firebase-uid',
            email='email1@example.com',
            username='user1'
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create(
                firebase_uid='unique-firebase-uid',
                email='email2@example.com',
                username='user2'
            )
    
    def test_user_admin_flag(self):
        """Test admin flag can be set."""
        user = User.objects.create(
            firebase_uid='admin-uid',
            email='admin@example.com',
            username='adminuser',
            is_admin=True
        )
        
        assert user.is_admin is True
    
    def test_user_banned_flag(self):
        """Test banned flag can be set."""
        user = User.objects.create(
            firebase_uid='banned-uid',
            email='banned@example.com',
            username='banneduser',
            is_banned=True
        )
        
        assert user.is_banned is True


@pytest.mark.django_db
class TestUserProfileModel:
    """Test UserProfile model."""
    
    def test_user_profile_creation(self):
        """Test creating a user profile."""
        user = User.objects.create(
            firebase_uid='profile-uid',
            email='profile@example.com',
            username='profileuser'
        )
        
        profile = UserProfile.objects.create(
            user=user,
            display_name='Display Name',
            bio='This is my bio',
            location='Paris, France'
        )
        
        assert profile.user == user
        assert profile.display_name == 'Display Name'
        assert profile.bio == 'This is my bio'
        assert profile.location == 'Paris, France'
    
    def test_user_profile_defaults(self):
        """Test user profile default values."""
        user = User.objects.create(
            firebase_uid='default-uid',
            email='default@example.com',
            username='defaultuser'
        )
        
        profile = UserProfile.objects.create(user=user)

        assert profile.display_name is None
        assert profile.bio == ''
        assert profile.location == ''
        assert not profile.profile_picture
    
    def test_user_profile_one_to_one(self):
        """Test user can only have one profile."""
        user = User.objects.create(
            firebase_uid='one-profile-uid',
            email='oneprofile@example.com',
            username='oneprofileuser'
        )
        
        UserProfile.objects.create(user=user)
        
        # Attempting to create second profile should fail
        with pytest.raises(IntegrityError):
            UserProfile.objects.create(user=user)
    
    def test_profile_cascade_on_user_delete(self):
        """Test profile is deleted when user is deleted."""
        user = User.objects.create(
            firebase_uid='cascade-uid',
            email='cascade@example.com',
            username='cascadeuser'
        )
        
        profile = UserProfile.objects.create(user=user)
        profile_id = profile.profile_id

        # Delete user
        user.delete()

        # Profile should be deleted
        assert not UserProfile.objects.filter(profile_id=profile_id).exists()


@pytest.mark.django_db
class TestUserSettingsModel:
    """Test UserSettings model."""
    
    def test_user_settings_defaults(self):
        """Test user settings default values."""
        user = User.objects.create(
            firebase_uid='settings-uid',
            email='settings@example.com',
            username='settingsuser'
        )
        
        settings = UserSettings.objects.create(user=user)

        assert settings.email_notifications is True
        assert settings.language == 'fr'
    
    def test_user_settings_custom_values(self):
        """Test setting custom values for user settings."""
        user = User.objects.create(
            firebase_uid='custom-settings-uid',
            email='customsettings@example.com',
            username='customsettingsuser'
        )
        
        settings = UserSettings.objects.create(
            user=user,
            email_notifications=False,
            language='en'
        )

        assert settings.email_notifications is False
        assert settings.language == 'en'
    
    def test_settings_one_to_one(self):
        """Test user can only have one settings object."""
        user = User.objects.create(
            firebase_uid='one-settings-uid',
            email='onesettings@example.com',
            username='onesettingsuser'
        )
        
        UserSettings.objects.create(user=user)
        
        # Attempting to create second settings should fail
        with pytest.raises(IntegrityError):
            UserSettings.objects.create(user=user)
    
    def test_settings_cascade_on_user_delete(self):
        """Test settings are deleted when user is deleted."""
        user = User.objects.create(
            firebase_uid='settings-cascade-uid',
            email='settingscascade@example.com',
            username='settingscascadeuser'
        )
        
        settings = UserSettings.objects.create(user=user)
        settings_id = settings.settings_id

        # Delete user
        user.delete()

        # Settings should be deleted
        assert not UserSettings.objects.filter(settings_id=settings_id).exists()


@pytest.mark.django_db
class TestBlockModel:
    """Test Block model."""
    
    def test_block_creation(self):
        """Test creating a block."""
        blocker = User.objects.create(
            firebase_uid='blocker-uid',
            email='blocker@example.com',
            username='blocker'
        )
        blocked = User.objects.create(
            firebase_uid='blocked-uid',
            email='blocked@example.com',
            username='blocked'
        )
        
        block = Block.objects.create(
            blocker=blocker,
            blocked=blocked
        )
        
        assert block.blocker == blocker
        assert block.blocked == blocked
        assert block.created_at is not None
    
    def test_block_unique_constraint(self):
        """Test same user pair can only be blocked once."""
        blocker = User.objects.create(
            firebase_uid='unique-blocker-uid',
            email='uniqueblocker@example.com',
            username='uniqueblocker'
        )
        blocked = User.objects.create(
            firebase_uid='unique-blocked-uid',
            email='uniqueblocked@example.com',
            username='uniqueblocked'
        )
        
        Block.objects.create(blocker=blocker, blocked=blocked)
        
        # Attempting to create duplicate block should fail
        with pytest.raises(IntegrityError):
            Block.objects.create(blocker=blocker, blocked=blocked)
    
    def test_block_str_representation(self):
        """Test __str__ method."""
        blocker = User.objects.create(
            firebase_uid='str-blocker-uid',
            email='strblocker@example.com',
            username='strblocker'
        )
        blocked = User.objects.create(
            firebase_uid='str-blocked-uid',
            email='strblocked@example.com',
            username='strblocked'
        )
        
        block = Block.objects.create(blocker=blocker, blocked=blocked)
        
        assert str(block) == 'strblocker blocks strblocked'
    
    def test_block_cascade_on_user_delete(self):
        """Test blocks are deleted when user is deleted."""
        blocker = User.objects.create(
            firebase_uid='cascade-blocker-uid',
            email='cascadeblocker@example.com',
            username='cascadeblocker'
        )
        blocked = User.objects.create(
            firebase_uid='cascade-blocked-uid',
            email='cascadeblocked@example.com',
            username='cascadeblocked'
        )
        
        block = Block.objects.create(blocker=blocker, blocked=blocked)
        block_id = block.block_id
        
        # Delete blocker
        blocker.delete()
        
        # Block should be deleted
        assert not Block.objects.filter(block_id=block_id).exists()


@pytest.mark.django_db
class TestFollowModel:
    """Test Follow model."""
    
    def test_follow_creation_accepted(self):
        """Test creating an accepted follow."""
        follower = User.objects.create(
            firebase_uid='follower-uid',
            email='follower@example.com',
            username='follower'
        )
        following = User.objects.create(
            firebase_uid='following-uid',
            email='following@example.com',
            username='following'
        )
        
        follow = Follow.objects.create(
            follower=follower,
            following=following,
            status='accepted'
        )
        
        assert follow.follower == follower
        assert follow.following == following
        assert follow.status == 'accepted'
        assert follow.created_at is not None
    
    def test_follow_creation_pending(self):
        """Test creating a pending follow request."""
        follower = User.objects.create(
            firebase_uid='pending-follower-uid',
            email='pendingfollower@example.com',
            username='pendingfollower'
        )
        following = User.objects.create(
            firebase_uid='pending-following-uid',
            email='pendingfollowing@example.com',
            username='pendingfollowing'
        )
        
        follow = Follow.objects.create(
            follower=follower,
            following=following,
            status='pending'
        )
        
        assert follow.status == 'pending'
    
    def test_follow_unique_constraint(self):
        """Test same user pair can only have one follow relationship."""
        follower = User.objects.create(
            firebase_uid='unique-follower-uid',
            email='uniquefollower@example.com',
            username='uniquefollower'
        )
        following = User.objects.create(
            firebase_uid='unique-following-uid',
            email='uniquefollowing@example.com',
            username='uniquefollowing'
        )
        
        Follow.objects.create(follower=follower, following=following)
        
        # Attempting to create duplicate follow should fail
        with pytest.raises(IntegrityError):
            Follow.objects.create(follower=follower, following=following)
    
    def test_follow_str_representation(self):
        """Test __str__ method."""
        follower = User.objects.create(
            firebase_uid='str-follower-uid',
            email='strfollower@example.com',
            username='strfollower'
        )
        following = User.objects.create(
            firebase_uid='str-following-uid',
            email='strfollowing@example.com',
            username='strfollowing'
        )
        
        follow = Follow.objects.create(
            follower=follower,
            following=following,
            status='accepted'
        )

        assert str(follow) == 'strfollower follows strfollowing'
    
    def test_follow_cascade_on_user_delete(self):
        """Test follows are deleted when user is deleted."""
        follower = User.objects.create(
            firebase_uid='cascade-follower-uid',
            email='cascadefollower@example.com',
            username='cascadefollower'
        )
        following = User.objects.create(
            firebase_uid='cascade-following-uid',
            email='cascadefollowing@example.com',
            username='cascadefollowing'
        )
        
        follow = Follow.objects.create(follower=follower, following=following)
        follow_id = follow.follow_id
        
        # Delete follower
        follower.delete()
        
        # Follow should be deleted
        assert not Follow.objects.filter(follow_id=follow_id).exists()


@pytest.mark.django_db
class TestUserRepositoryIntegration:
    """Test UserRepository creates related objects correctly."""
    
    def test_create_user_creates_profile_and_settings(self):
        """Test that UserRepository.create also creates profile and settings."""
        user = UserRepository.create(
            firebase_uid='integration-uid',
            email='integration@example.com',
            username='integrationuser'
        )
        
        # Check user was created
        assert user is not None
        assert user.username == 'integrationuser'
        
        # Check profile was created
        profile = UserProfile.objects.filter(user=user).first()
        assert profile is not None

        # Check settings were created
        settings = UserSettings.objects.filter(user=user).first()
        assert settings is not None
        assert settings.email_notifications is True

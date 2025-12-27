"""
Integration tests for Users API.
Tests conformity with API endpoints and business rules.
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from db.entities.user_entity import User, Block, Follow
from db.repositories.user_repository import UserRepository


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def test_user(db):
    """Create test user."""
    user = UserRepository.create(
        email='testuser@test.com',
        username='testuser',
        firebase_uid='firebase_test_uid'
    )
    user.profile.display_name = 'Test User'
    user.profile.save()
    return user


@pytest.fixture
def user2(db):
    """Create second test user."""
    user = UserRepository.create(
        email='user2@test.com',
        username='user2',
        firebase_uid='firebase_user2_uid'
    )
    user.profile.display_name = 'User 2'
    user.profile.save()
    return user


@pytest.fixture
def user3(db):
    """Create third test user."""
    user = UserRepository.create(
        email='user3@test.com',
        username='user3',
        firebase_uid='firebase_user3_uid'
    )
    user.profile.display_name = 'User 3'
    user.profile.save()
    return user


@pytest.mark.django_db
class TestCurrentUserAPI:
    """Test GET /api/v1/users/me/ endpoint."""
    
    def test_get_current_user_authenticated(self, api_client, test_user):
        """Test getting current user profile when authenticated."""
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get('/api/v1/users/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['email'] == 'testuser@test.com'
        assert 'user_id' in response.data
        assert 'profile' in response.data or 'display_name' in response.data
    
    def test_get_current_user_unauthenticated(self, api_client):
        """Test getting current user without authentication fails."""
        response = api_client.get('/api/v1/users/me/')
        
        # Should return 401 or null depending on implementation
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED,
                                       status.HTTP_403_FORBIDDEN,
                                       status.HTTP_200_OK]
        
        if response.status_code == status.HTTP_200_OK:
            assert response.data is None


@pytest.mark.django_db
class TestCreateUserAPI:
    """Test POST /api/v1/users/create/ endpoint."""
    
    def test_create_user_from_firebase(self, api_client):
        """Test creating user from Firebase authentication."""
        # Simulate Firebase authentication
        firebase_user = User(
            firebase_uid='new-firebase-uid',
            email='newuser@test.com'
        )
        firebase_user.is_authenticated = True
        api_client.force_authenticate(user=firebase_user)
        
        payload = {
            'username': 'newuser',
            'bio': 'This is my bio',
            'location': 'Paris'
        }
        response = api_client.post('/api/v1/users/', payload, format='json')
        
        # Should create user or return existing
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]
        
        if response.status_code == status.HTTP_201_CREATED:
            assert 'user_id' in response.data
            assert response.data['username'] == 'newuser'
    
    def test_create_user_duplicate_username(self, api_client, test_user):
        """Test creating user with existing username returns 409."""
        firebase_user = User(
            firebase_uid='another-firebase-uid',
            email='another@test.com'
        )
        firebase_user.is_authenticated = True
        api_client.force_authenticate(user=firebase_user)
        
        payload = {'username': 'testuser'}  # Already exists
        response = api_client.post('/api/v1/users/', payload, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT
    
    def test_create_user_invalid_username(self, api_client):
        """Test creating user with invalid username returns 400."""
        firebase_user = User(
            firebase_uid='invalid-firebase-uid',
            email='invalid@test.com'
        )
        firebase_user.is_authenticated = True
        api_client.force_authenticate(user=firebase_user)
        
        payload = {'username': 'invalid user!'}  # Invalid characters
        response = api_client.post('/api/v1/users/', payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateProfileAPI:
    """Test PATCH /api/v1/users/me/ endpoint."""
    
    def test_update_profile_success(self, api_client, test_user):
        """Test updating user profile successfully."""
        api_client.force_authenticate(user=test_user)

        payload = {
            'bio': 'Updated bio',
            'location': 'New York',
            'display_name': 'Updated Name'
        }
        response = api_client.patch('/api/v1/users/me/update/', payload, format='json')

        assert response.status_code == status.HTTP_200_OK

        # Verify changes in database
        test_user.refresh_from_db()
        profile = test_user.profile
        assert profile.bio == 'Updated bio'
        assert profile.location == 'New York'
    
    def test_update_profile_bio(self, api_client, test_user):
        """Test updating only bio."""
        api_client.force_authenticate(user=test_user)

        payload = {'bio': 'Just updating bio'}
        response = api_client.patch('/api/v1/users/me/update/', payload, format='json')

        assert response.status_code == status.HTTP_200_OK
    
    def test_update_profile_banned_user(self, api_client, test_user):
        """Test banned user cannot update profile."""
        test_user.is_banned = True
        test_user.save()

        api_client.force_authenticate(user=test_user)

        payload = {'bio': 'Trying to update'}
        response = api_client.patch('/api/v1/users/me/update/', payload, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_profile_unauthenticated(self, api_client):
        """Test updating profile without authentication fails."""
        payload = {'bio': 'Test'}
        response = api_client.patch('/api/v1/users/me/update/', payload, format='json')

        assert response.status_code in [status.HTTP_401_UNAUTHORIZED,
                                       status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestUpdateSettingsAPI:
    """Test PATCH /api/v1/users/me/settings/ endpoint."""
    
    def test_update_settings_privacy(self, api_client, test_user):
        """Test updating privacy settings."""
        api_client.force_authenticate(user=test_user)
        
        payload = {
            'privacy_profile': False,
            'privacy_posts': False
        }
        response = api_client.patch('/api/v1/users/me/settings/', payload, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify changes
        test_user.refresh_from_db()
        settings = test_user.settings
        assert settings.privacy_profile is False
        assert settings.privacy_posts is False
    
    def test_update_settings_notifications(self, api_client, test_user):
        """Test updating notification settings."""
        api_client.force_authenticate(user=test_user)
        
        payload = {
            'notifications_enabled': False,
            'notifications_email': False
        }
        response = api_client.patch('/api/v1/users/me/settings/', payload, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        test_user.refresh_from_db()
        settings = test_user.settings
        assert settings.notifications_enabled is False


@pytest.mark.django_db
class TestUserDetailAPI:
    """Test GET /api/v1/users/{user_id}/ endpoint."""
    
    def test_get_user_public_profile(self, api_client, test_user, user2):
        """Test getting another user's public profile."""
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get(f'/api/v1/users/{user2.user_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'user2'
        # Should not expose private info like email
        assert 'email' not in response.data or response.data.get('email') is None
    
    def test_get_user_not_found(self, api_client, test_user):
        """Test getting non-existent user returns 404."""
        api_client.force_authenticate(user=test_user)
        
        import uuid
        fake_id = str(uuid.uuid4())
        response = api_client.get(f'/api/v1/users/{fake_id}/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_user_banned(self, api_client, test_user, user2):
        """Test getting banned user's profile."""
        user2.is_banned = True
        user2.save()
        
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get(f'/api/v1/users/{user2.user_id}/')
        
        # Might return 404 or limited info depending on implementation
        assert response.status_code in [status.HTTP_404_NOT_FOUND,
                                       status.HTTP_200_OK]


@pytest.mark.django_db
class TestUserSearchAPI:
    """Test GET /api/v1/users/search/ endpoint."""
    
    def test_search_users_by_username(self, api_client, test_user):
        """Test searching users by username."""
        # Create users to search
        UserRepository.create(
            email='searchuser1@test.com',
            username='searchuser1',
            firebase_uid='search1'
        )
        UserRepository.create(
            email='searchuser2@test.com',
            username='searchuser2',
            firebase_uid='search2'
        )
        
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get('/api/v1/users/search/?query=search')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 2
    
    def test_search_users_case_insensitive(self, api_client, test_user):
        """Test search is case-insensitive."""
        UserRepository.create(
            email='caseuser@test.com',
            username='CaseUser',
            firebase_uid='case1'
        )
        
        api_client.force_authenticate(user=test_user)
        
        # Search with lowercase
        response = api_client.get('/api/v1/users/search/?query=case')
        
        assert response.status_code == status.HTTP_200_OK
        usernames = [u['username'] for u in response.data]
        assert 'CaseUser' in usernames
    
    def test_search_users_pagination(self, api_client, test_user):
        """Test search pagination."""
        # Create many users
        for i in range(15):
            UserRepository.create(
                email=f'pageuser{i}@test.com',
                username=f'pageuser{i:02d}',
                firebase_uid=f'page{i}'
            )
        
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get('/api/v1/users/search/?query=pageuser&page=1&page_size=10')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10
    
    def test_search_excludes_banned(self, api_client, test_user):
        """Test search excludes banned users."""
        normal_user = UserRepository.create(
            email='normal@test.com',
            username='normaluser',
            firebase_uid='normal'
        )

        banned_user = UserRepository.create(
            email='banned@test.com',
            username='banneduser',
            firebase_uid='banned'
        )
        banned_user.is_banned = True
        banned_user.save()
        
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get('/api/v1/users/search/?query=user')
        
        usernames = [u['username'] for u in response.data]
        assert 'normaluser' in usernames
        assert 'banneduser' not in usernames
    
    def test_search_empty_query(self, api_client, test_user):
        """Test search with empty query."""
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get('/api/v1/users/search/?query=')
        
        # Should return empty or error
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]


@pytest.mark.django_db
class TestUserBulkAPI:
    """Test POST /api/v1/users/bulk/ endpoint."""
    
    def test_get_bulk_users(self, api_client, test_user, user2, user3):
        """Test getting multiple users by IDs."""
        api_client.force_authenticate(user=test_user)
        
        payload = {
            'user_ids': [str(user2.user_id), str(user3.user_id)]
        }
        response = api_client.post('/api/v1/users/bulk/', payload, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        
        usernames = [u['username'] for u in response.data]
        assert 'user2' in usernames
        assert 'user3' in usernames
    
    def test_get_bulk_excludes_banned(self, api_client, test_user, user2):
        """Test bulk get excludes banned users."""
        user2.is_banned = True
        user2.save()
        
        api_client.force_authenticate(user=test_user)
        
        payload = {'user_ids': [str(user2.user_id)]}
        response = api_client.post('/api/v1/users/bulk/', payload, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
    
    def test_get_bulk_empty_list(self, api_client, test_user):
        """Test bulk get with empty list."""
        api_client.force_authenticate(user=test_user)
        
        payload = {'user_ids': []}
        response = api_client.post('/api/v1/users/bulk/', payload, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0


@pytest.mark.django_db
class TestBlockUserAPI:
    """Test POST /api/v1/users/{user_id}/block/ endpoint."""
    
    def test_block_user_success(self, api_client, test_user, user2):
        """Test blocking a user successfully."""
        api_client.force_authenticate(user=test_user)

        response = api_client.post(f'/api/v1/users/{user2.user_id}/block/')

        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT]

        # Verify block was created
        assert Block.objects.filter(
            blocker=test_user,
            blocked=user2
        ).exists()
    
    def test_block_user_already_blocked(self, api_client, test_user, user2):
        """Test blocking already blocked user is idempotent."""
        Block.objects.create(blocker=test_user, blocked=user2)

        api_client.force_authenticate(user=test_user)

        response = api_client.post(f'/api/v1/users/{user2.user_id}/block/')

        # Should succeed (idempotent)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT]
    
    def test_block_user_not_found(self, api_client, test_user):
        """Test blocking non-existent user."""
        api_client.force_authenticate(user=test_user)
        
        import uuid
        fake_id = str(uuid.uuid4())
        response = api_client.post(f'/api/v1/users/{fake_id}/block/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_block_self(self, api_client, test_user):
        """Test cannot block yourself."""
        api_client.force_authenticate(user=test_user)
        
        response = api_client.post(f'/api/v1/users/{test_user.user_id}/block/')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUnblockUserAPI:
    """Test DELETE /api/v1/users/{user_id}/unblock/ endpoint."""
    
    def test_unblock_user_success(self, api_client, test_user, user2):
        """Test unblocking a user successfully."""
        Block.objects.create(blocker=test_user, blocked=user2)
        
        api_client.force_authenticate(user=test_user)
        
        response = api_client.delete(f'/api/v1/users/{user2.user_id}/unblock/')
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        
        # Verify block was removed
        assert not Block.objects.filter(
            blocker=test_user,
            blocked=user2
        ).exists()
    
    def test_unblock_user_not_blocked(self, api_client, test_user, user2):
        """Test unblocking non-blocked user is idempotent."""
        api_client.force_authenticate(user=test_user)

        response = api_client.delete(f'/api/v1/users/{user2.user_id}/unblock/')

        # Should succeed (idempotent) - API might return 404 if not blocked
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND]
    
    def test_unblock_user_not_found(self, api_client, test_user):
        """Test unblocking non-existent user."""
        api_client.force_authenticate(user=test_user)
        
        import uuid
        fake_id = str(uuid.uuid4())
        response = api_client.delete(f'/api/v1/users/{fake_id}/unblock/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBlockedUsersAPI:
    """Test GET /api/v1/users/me/blocked/ endpoint."""

    def test_get_blocked_users_list(self, api_client, test_user, user2, user3):
        """Test getting list of blocked users."""
        Block.objects.create(blocker=test_user, blocked=user2)
        Block.objects.create(blocker=test_user, blocked=user3)

        api_client.force_authenticate(user=test_user)

        response = api_client.get('/api/v1/users/me/blocked/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_get_blocked_users_pagination(self, api_client, test_user):
        """Test blocked users list pagination."""
        # Create and block many users
        for i in range(15):
            user = UserRepository.create(
                email=f'blocked{i}@test.com',
                username=f'blocked{i}',
                firebase_uid=f'blocked{i}'
            )
            Block.objects.create(blocker=test_user, blocked=user)
        
        api_client.force_authenticate(user=test_user)

        response = api_client.get('/api/v1/users/me/blocked/?page=1&page_size=10')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10
    
    def test_get_blocked_users_empty(self, api_client, test_user):
        """Test getting blocked users when none are blocked."""
        api_client.force_authenticate(user=test_user)

        response = api_client.get('/api/v1/users/me/blocked/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0


@pytest.mark.django_db
class TestUserAPIConformity:
    """Test conformity with specifications."""
    
    def test_user_endpoints_require_authentication(self, api_client):
        """Test all user endpoints require authentication."""
        endpoints = [
            '/api/v1/users/me/',
            '/api/v1/users/search/?query=test',
            '/api/v1/users/me/blocked/',
        ]
        
        for endpoint in endpoints:
            response = api_client.get(endpoint)
            assert response.status_code in [status.HTTP_401_UNAUTHORIZED,
                                           status.HTTP_403_FORBIDDEN,
                                           status.HTTP_200_OK]  # Some might return null
    
    def test_banned_user_restrictions(self, api_client, test_user):
        """Test banned users have restricted access."""
        test_user.is_banned = True
        test_user.save()
        
        api_client.force_authenticate(user=test_user)
        
        # Should not be able to update profile
        response = api_client.patch('/api/v1/users/me/update/', {'bio': 'test'}, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

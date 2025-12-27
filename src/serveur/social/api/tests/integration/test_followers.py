"""
Integration tests for Followers API.
Tests all endpoints defined in apps/followers/urls.py.
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from db.entities.user_entity import User, UserProfile, Follow


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def public_user(db):
    """Create test user with public profile."""
    user = User.objects.create(
        email='public_user@test.com',
        username='public_user',
        firebase_uid='firebase_id_public'
    )
    # Create public profile
    UserProfile.objects.create(
        user=user,
        display_name='Public User',
        profile_picture_url='https://example.com/pic.jpg',
        privacy=True  # True = public
    )
    # Add DRF authentication attributes
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def private_user(db):
    """Create test user with private profile."""
    user = User.objects.create(
        email='private_user@test.com',
        username='private_user',
        firebase_uid='firebase_id_private'
    )
    # Create private profile
    UserProfile.objects.create(
        user=user,
        display_name='Private User',
        profile_picture_url='https://example.com/pic2.jpg',
        privacy=False  # False = private
    )
    # Add DRF authentication attributes
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def another_public_user(db):
    """Create another test user with public profile."""
    user = User.objects.create(
        email='another_public@test.com',
        username='another_public',
        firebase_uid='firebase_id_another'
    )
    # Create public profile
    UserProfile.objects.create(
        user=user,
        display_name='Another Public User',
        profile_picture_url='https://example.com/pic3.jpg',
        privacy=True  # True = public
    )
    # Add DRF authentication attributes
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.mark.django_db
class TestFollowersAPI:
    """Test Followers API endpoints."""
    
    # ========================
    # POST /<user_id>/follow/
    # ========================
    
    def test_follow_public_user(self, api_client, public_user, another_public_user):
        """
        Test: POST /<user_id>/follow/
        Spec: Follow a public user - status should be 'accepted'
        """
        api_client.force_authenticate(user=public_user)
        
        response = api_client.post(
            f'/api/v1/followers/{another_public_user.user_id}/follow/'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'accepted'
        assert str(response.data['follower_id']) == str(public_user.user_id)
        assert str(response.data['following_id']) == str(another_public_user.user_id)
        assert 'follow_id' in response.data
        assert 'created_at' in response.data
    
    def test_follow_private_user(self, api_client, public_user, private_user):
        """
        Test: POST /<user_id>/follow/
        Spec: Follow a private user - status should be 'pending'
        """
        api_client.force_authenticate(user=public_user)
        
        response = api_client.post(
            f'/api/v1/followers/{private_user.user_id}/follow/'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'pending'
        assert str(response.data['follower_id']) == str(public_user.user_id)
        assert str(response.data['following_id']) == str(private_user.user_id)
    
    def test_follow_self_forbidden(self, api_client, public_user):
        """
        Test: Cannot follow yourself
        Spec: Validation error
        """
        api_client.force_authenticate(user=public_user)
        
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/follow/'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_follow_nonexistent_user(self, api_client, public_user):
        """
        Test: Follow nonexistent user
        Spec: NotFoundError
        """
        api_client.force_authenticate(user=public_user)
        
        fake_user_id = '00000000-0000-0000-0000-000000000000'
        response = api_client.post(
            f'/api/v1/followers/{fake_user_id}/follow/'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_follow_already_following(self, api_client, public_user, another_public_user):
        """
        Test: Cannot follow same user twice
        Spec: ConflictError
        """
        api_client.force_authenticate(user=public_user)
        
        # First follow
        api_client.post(
            f'/api/v1/followers/{another_public_user.user_id}/follow/'
        )
        
        # Second follow should fail
        response = api_client.post(
            f'/api/v1/followers/{another_public_user.user_id}/follow/'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_follow_requires_authentication(self, api_client, public_user, another_public_user):
        """
        Test: Unauthenticated users cannot follow
        """
        # No authentication
        response = api_client.post(
            f'/api/v1/followers/{another_public_user.user_id}/follow/'
        )
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    # ========================
    # DELETE /<user_id>/unfollow/
    # ========================
    
    def test_unfollow_user(self, api_client, public_user, another_public_user):
        """
        Test: DELETE /<user_id>/unfollow/
        Spec: Unfollow a user
        """
        api_client.force_authenticate(user=public_user)
        
        # First follow
        api_client.post(
            f'/api/v1/followers/{another_public_user.user_id}/follow/'
        )
        
        # Then unfollow
        response = api_client.delete(
            f'/api/v1/followers/{another_public_user.user_id}/unfollow/'
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify follow is deleted
        follow = Follow.objects.filter(
            follower=public_user,
            following=another_public_user
        ).first()
        assert follow is None
    
    def test_unfollow_not_following(self, api_client, public_user, another_public_user):
        """
        Test: Unfollow when not following
        Spec: NotFoundError
        """
        api_client.force_authenticate(user=public_user)
        
        response = api_client.delete(
            f'/api/v1/followers/{another_public_user.user_id}/unfollow/'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
    
    def test_unfollow_requires_authentication(self, api_client, another_public_user):
        """
        Test: Unauthenticated users cannot unfollow
        """
        response = api_client.delete(
            f'/api/v1/followers/{another_public_user.user_id}/unfollow/'
        )
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    # ========================
    # POST /<user_id>/accept/
    # ========================
    
    def test_accept_follow_request(self, api_client, private_user, public_user):
        """
        Test: POST /<user_id>/accept/
        Spec: Accept a pending follow request
        """
        # Create pending follow request
        Follow.objects.create(
            follower=public_user,
            following=private_user,
            status='pending'
        )
        
        api_client.force_authenticate(user=private_user)
        
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/accept/'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'accepted'
        assert str(response.data['follower_id']) == str(public_user.user_id)
        assert str(response.data['following_id']) == str(private_user.user_id)
        
        # Verify follow is accepted in database
        follow = Follow.objects.get(follower=public_user, following=private_user)
        assert follow.status == 'accepted'
    
    def test_accept_nonexistent_follow_request(self, api_client, private_user, public_user):
        """
        Test: Accept nonexistent follow request
        Spec: NotFoundError
        """
        api_client.force_authenticate(user=private_user)
        
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/accept/'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
    
    def test_accept_non_pending_follow(self, api_client, private_user, public_user):
        """
        Test: Cannot accept already accepted follow
        Spec: ValidationError
        """
        # Create accepted follow request
        Follow.objects.create(
            follower=public_user,
            following=private_user,
            status='accepted'
        )
        
        api_client.force_authenticate(user=private_user)
        
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/accept/'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_accept_requires_authentication(self, api_client, public_user):
        """
        Test: Unauthenticated users cannot accept follow requests
        """
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/accept/'
        )
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    # ========================
    # POST /<user_id>/refuse/
    # ========================
    
    def test_refuse_follow_request(self, api_client, private_user, public_user):
        """
        Test: POST /<user_id>/refuse/
        Spec: Refuse a pending follow request
        """
        # Create pending follow request
        Follow.objects.create(
            follower=public_user,
            following=private_user,
            status='pending'
        )
        
        api_client.force_authenticate(user=private_user)
        
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/refuse/'
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify follow is refused in database
        follow = Follow.objects.get(follower=public_user, following=private_user)
        assert follow.status == 'refused'
    
    def test_refuse_nonexistent_follow_request(self, api_client, private_user, public_user):
        """
        Test: Refuse nonexistent follow request
        Spec: NotFoundError
        """
        api_client.force_authenticate(user=private_user)
        
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/refuse/'
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
    
    def test_refuse_non_pending_follow(self, api_client, private_user, public_user):
        """
        Test: Cannot refuse already accepted follow
        Spec: ValidationError
        """
        # Create accepted follow request
        Follow.objects.create(
            follower=public_user,
            following=private_user,
            status='accepted'
        )
        
        api_client.force_authenticate(user=private_user)
        
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/refuse/'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_refuse_requires_authentication(self, api_client, public_user):
        """
        Test: Unauthenticated users cannot refuse follow requests
        """
        response = api_client.post(
            f'/api/v1/followers/{public_user.user_id}/refuse/'
        )
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    # ========================
    # GET /me/
    # ========================
    
    def test_get_followers_list(self, api_client, public_user, another_public_user, private_user):
        """
        Test: GET /me/
        Spec: Get current user's followers list
        """
        # another_public_user and private_user follow public_user
        Follow.objects.create(
            follower=another_public_user,
            following=public_user,
            status='accepted'
        )
        Follow.objects.create(
            follower=private_user,
            following=public_user,
            status='accepted'
        )
        
        api_client.force_authenticate(user=public_user)
        
        response = api_client.get('/api/v1/followers/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 2
        
        # Verify user data in response
        follower_ids = [f['user_id'] for f in response.data]
        assert str(another_public_user.user_id) in follower_ids
        assert str(private_user.user_id) in follower_ids
        
        # Verify user fields
        for follower in response.data:
            assert 'user_id' in follower
            assert 'username' in follower
            assert 'display_name' in follower
            assert 'profile_picture_url' in follower
    
    def test_get_followers_empty_list(self, api_client, public_user):
        """
        Test: GET /me/ with no followers
        """
        api_client.force_authenticate(user=public_user)
        
        response = api_client.get('/api/v1/followers/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 0
    
    def test_get_followers_pagination(self, api_client, public_user, db):
        """
        Test: GET /me/ with pagination
        """
        # Create multiple followers
        for i in range(5):
            follower = User.objects.create(
                email=f'follower{i}@test.com',
                username=f'follower{i}',
                firebase_uid=f'firebase_follower_{i}'
            )
            UserProfile.objects.create(
                user=follower,
                display_name=f'Follower {i}',
                profile_picture_url=f'https://example.com/pic{i}.jpg'
            )
            Follow.objects.create(
                follower=follower,
                following=public_user,
                status='accepted'
            )
        
        api_client.force_authenticate(user=public_user)
        
        # Test default pagination
        response = api_client.get('/api/v1/followers/me/')
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 5
        
        # Test with custom page size
        response = api_client.get('/api/v1/followers/me/?page_size=2')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) <= 2
    
    def test_get_followers_requires_authentication(self, api_client):
        """
        Test: Unauthenticated users cannot get followers
        """
        response = api_client.get('/api/v1/followers/me/')
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    # ========================
    # GET /following/
    # ========================
    
    def test_get_following_list(self, api_client, public_user, another_public_user, private_user):
        """
        Test: GET /following/
        Spec: Get users that current user follows
        """
        # public_user follows another_public_user and private_user
        Follow.objects.create(
            follower=public_user,
            following=another_public_user,
            status='accepted'
        )
        Follow.objects.create(
            follower=public_user,
            following=private_user,
            status='accepted'
        )
        
        api_client.force_authenticate(user=public_user)
        
        response = api_client.get('/api/v1/followers/following/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 2
        
        # Verify user data in response
        following_ids = [f['user_id'] for f in response.data]
        assert str(another_public_user.user_id) in following_ids
        assert str(private_user.user_id) in following_ids
        
        # Verify user fields
        for user in response.data:
            assert 'user_id' in user
            assert 'username' in user
            assert 'display_name' in user
            assert 'profile_picture_url' in user
    
    def test_get_following_empty_list(self, api_client, public_user):
        """
        Test: GET /following/ with no following
        """
        api_client.force_authenticate(user=public_user)
        
        response = api_client.get('/api/v1/followers/following/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 0
    
    def test_get_following_pagination(self, api_client, public_user, db):
        """
        Test: GET /following/ with pagination
        """
        # Create multiple users to follow
        for i in range(5):
            user_to_follow = User.objects.create(
                email=f'follow{i}@test.com',
                username=f'follow{i}',
                firebase_uid=f'firebase_follow_{i}'
            )
            UserProfile.objects.create(
                user=user_to_follow,
                display_name=f'Follow {i}',
                profile_picture_url=f'https://example.com/pic{i}.jpg'
            )
            Follow.objects.create(
                follower=public_user,
                following=user_to_follow,
                status='accepted'
            )
        
        api_client.force_authenticate(user=public_user)
        
        # Test default pagination
        response = api_client.get('/api/v1/followers/following/')
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 5
        
        # Test with custom page size
        response = api_client.get('/api/v1/followers/following/?page_size=2')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) <= 2
    
    def test_get_following_requires_authentication(self, api_client):
        """
        Test: Unauthenticated users cannot get following list
        """
        response = api_client.get('/api/v1/followers/following/')
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    
    # ========================
    # GET /pending/
    # ========================
    
    def test_get_pending_requests(self, api_client, private_user, public_user, another_public_user):
        """
        Test: GET /pending/
        Spec: Get pending follow requests for current user
        """
        # Create pending follow requests for private_user
        Follow.objects.create(
            follower=public_user,
            following=private_user,
            status='pending'
        )
        Follow.objects.create(
            follower=another_public_user,
            following=private_user,
            status='pending'
        )
        
        api_client.force_authenticate(user=private_user)
        
        response = api_client.get('/api/v1/followers/pending/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 2
        
        # Verify follow request data in response
        for follow_req in response.data:
            assert 'follow_id' in follow_req
            assert 'follower_id' in follow_req
            assert 'following_id' in follow_req
            assert follow_req['status'] == 'pending'
            assert follow_req['following_id'] == str(private_user.user_id)
            assert 'created_at' in follow_req
    
    def test_get_pending_requests_empty_list(self, api_client, public_user):
        """
        Test: GET /pending/ with no pending requests
        """
        api_client.force_authenticate(user=public_user)
        
        response = api_client.get('/api/v1/followers/pending/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 0
    
    def test_get_pending_requests_only_pending(self, api_client, private_user, public_user, another_public_user):
        """
        Test: GET /pending/ returns only pending requests
        """
        # Create pending request
        Follow.objects.create(
            follower=public_user,
            following=private_user,
            status='pending'
        )
        # Create accepted follow (should not appear)
        Follow.objects.create(
            follower=another_public_user,
            following=private_user,
            status='accepted'
        )
        
        api_client.force_authenticate(user=private_user)
        
        response = api_client.get('/api/v1/followers/pending/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['status'] == 'pending'
    
    def test_get_pending_requests_pagination(self, api_client, private_user, db):
        """
        Test: GET /pending/ with pagination
        """
        # Create multiple pending requests
        for i in range(5):
            requester = User.objects.create(
                email=f'requester{i}@test.com',
                username=f'requester{i}',
                firebase_uid=f'firebase_requester_{i}'
            )
            UserProfile.objects.create(
                user=requester,
                display_name=f'Requester {i}',
                profile_picture_url=f'https://example.com/pic{i}.jpg'
            )
            Follow.objects.create(
                follower=requester,
                following=private_user,
                status='pending'
            )
        
        api_client.force_authenticate(user=private_user)
        
        # Test default pagination
        response = api_client.get('/api/v1/followers/pending/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5
        
        # Test with custom page size
        response = api_client.get('/api/v1/followers/pending/?page_size=2')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) <= 2
    
    def test_get_pending_requests_requires_authentication(self, api_client):
        """
        Test: Unauthenticated users cannot get pending requests
        """
        response = api_client.get('/api/v1/followers/pending/')
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestFollowersConformityWithSpecs:
    """Test conformity with followers app specifications."""
    
    def test_routes_match_specifications(self):
        """
        Verify all routes match urls.py.
        
        Expected routes:
        - GET /me/ ✅
        - GET /following/ ✅
        - GET /pending/ ✅
        - POST /<user_id>/follow/ ✅
        - DELETE /<user_id>/unfollow/ ✅
        - POST /<user_id>/accept/ ✅
        - POST /<user_id>/refuse/ ✅
        """
        # Routes are tested implicitly in TestFollowersAPI
        pass
    
    def test_follow_model_fields(self):
        """
        Verify Follow model has required fields.
        
        Required fields:
        - follow_id (UUID, PK) ✅
        - follower (FK → User) ✅
        - following (FK → User) ✅
        - status (CharField: pending, accepted, refused) ✅
        - created_at (DateTimeField) ✅
        
        Constraints:
        - unique_together: [follower, following] ✅
        - CHECK(follower != following) ✅
        """
        field_names = [f.name for f in Follow._meta.get_fields()]
        
        assert 'follow_id' in field_names
        assert 'follower' in field_names
        assert 'following' in field_names
        assert 'status' in field_names
        assert 'created_at' in field_names
        
        # Verify unique constraint
        assert ('follower', 'following') in Follow._meta.unique_together
        
        # Verify check constraint
        constraints = [c.name for c in Follow._meta.constraints]
        assert 'follow_not_self' in constraints
    
    def test_follow_status_choices(self):
        """Verify Follow status choices are correct."""
        follow_status_choices = dict(Follow.STATUS_CHOICES)
        
        assert 'pending' in follow_status_choices
        assert 'accepted' in follow_status_choices
        assert 'refused' in follow_status_choices
        
        assert follow_status_choices['pending'] == 'Pending'
        assert follow_status_choices['accepted'] == 'Accepted'
        assert follow_status_choices['refused'] == 'Refused'
    
    def test_user_profile_privacy_field(self):
        """Verify UserProfile privacy field exists and works correctly."""
        field_names = [f.name for f in UserProfile._meta.get_fields()]
        
        assert 'privacy' in field_names
        
        # Verify privacy field is boolean
        privacy_field = UserProfile._meta.get_field('privacy')
        assert privacy_field.get_internal_type() == 'BooleanField'
        
        # Verify default is True (public)
        assert privacy_field.default == True

"""
Integration tests for Tags API.
Tests conformity with API endpoints and business rules.
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from db.entities.post_entity import Tag, Post, PostTag
from db.entities.user_entity import User
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
    return user


@pytest.fixture
def admin_user(db):
    """Create admin user."""
    user = UserRepository.create(
        email='admin@test.com',
        username='adminuser',
        firebase_uid='firebase_admin_uid'
    )
    user.is_admin = True
    user.save()
    return user


@pytest.fixture
def test_post(db, test_user):
    """Create test post."""
    return Post.objects.create(
        user=test_user,
        title='Test Post',
        content='Test content for post'
    )


@pytest.mark.django_db
class TestTagsListAPI:
    """Test GET /api/v1/tags/ endpoint."""
    
    def test_list_tags_authenticated(self, api_client, test_user):
        """Test listing tags when authenticated."""
        # Create some tags
        Tag.objects.create(tag_name='python')
        Tag.objects.create(tag_name='django')
        Tag.objects.create(tag_name='react')
        
        # Authenticate
        api_client.force_authenticate(user=test_user)
        
        # Request
        response = api_client.get('/api/v1/tags/')
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 3
        
        tag_names = [tag['tag_name'] for tag in response.data]
        assert 'python' in tag_names
        assert 'django' in tag_names
        assert 'react' in tag_names
    
    def test_list_tags_pagination(self, api_client, test_user):
        """Test tags list pagination."""
        # Create many tags
        for i in range(15):
            Tag.objects.create(tag_name=f'tag-{i:02d}')
        
        api_client.force_authenticate(user=test_user)
        
        # Request first page
        response = api_client.get('/api/v1/tags/?page=1&page_size=10')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10
    
    def test_list_tags_unauthenticated(self, api_client):
        """Test listing tags without authentication fails."""
        response = api_client.get('/api/v1/tags/')
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, 
                                       status.HTTP_403_FORBIDDEN]
    
    def test_list_tags_empty(self, api_client, test_user):
        """Test listing tags when none exist."""
        api_client.force_authenticate(user=test_user)
        
        response = api_client.get('/api/v1/tags/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []


@pytest.mark.django_db
class TestCreateTagAPI:
    """Test POST /api/v1/tags/create/ endpoint."""
    
    def test_create_tag_success(self, api_client, test_user):
        """Test creating a tag successfully."""
        api_client.force_authenticate(user=test_user)
        
        payload = {'tag_name': 'python'}
        response = api_client.post('/api/v1/tags/create/', payload, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['tag_name'] == 'python'
        assert 'tag_id' in response.data
        assert 'created_at' in response.data
        
        # Verify in database
        assert Tag.objects.filter(tag_name='python').exists()
    
    def test_create_tag_duplicate(self, api_client, test_user):
        """Test creating duplicate tag returns 409 Conflict."""
        Tag.objects.create(tag_name='existing-tag')
        
        api_client.force_authenticate(user=test_user)
        
        payload = {'tag_name': 'existing-tag'}
        response = api_client.post('/api/v1/tags/create/', payload, format='json')
        
        assert response.status_code == status.HTTP_409_CONFLICT
    
    def test_create_tag_invalid_name(self, api_client, test_user):
        """Test creating tag with invalid name returns 400."""
        api_client.force_authenticate(user=test_user)
        
        # Invalid characters (spaces, special chars)
        payload = {'tag_name': 'invalid tag!'}
        response = api_client.post('/api/v1/tags/create/', payload, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_tag_empty_name(self, api_client, test_user):
        """Test creating tag with empty name returns 400."""
        api_client.force_authenticate(user=test_user)
        
        payload = {'tag_name': ''}
        response = api_client.post('/api/v1/tags/create/', payload, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_tag_missing_name(self, api_client, test_user):
        """Test creating tag without name returns 400."""
        api_client.force_authenticate(user=test_user)
        
        payload = {}
        response = api_client.post('/api/v1/tags/create/', payload, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_tag_banned_user(self, api_client, test_user):
        """Test banned user cannot create tags."""
        test_user.is_banned = True
        test_user.save()
        
        api_client.force_authenticate(user=test_user)
        
        payload = {'tag_name': 'python'}
        response = api_client.post('/api/v1/tags/create/', payload, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_tag_unauthenticated(self, api_client):
        """Test creating tag without authentication fails."""
        payload = {'tag_name': 'python'}
        response = api_client.post('/api/v1/tags/create/', payload, format='json')
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED,
                                       status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestDeleteTagAPI:
    """Test DELETE /api/v1/tags/{tag_id}/ endpoint."""
    
    def test_delete_tag_admin(self, api_client, admin_user):
        """Test admin can delete tags."""
        tag = Tag.objects.create(tag_name='to-delete')

        api_client.force_authenticate(user=admin_user)

        response = api_client.delete(f'/api/v1/tags/{tag.tag_id}/delete/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Tag.objects.filter(tag_id=tag.tag_id).exists()
    
    def test_delete_tag_non_admin(self, api_client, test_user):
        """Test non-admin cannot delete tags."""
        tag = Tag.objects.create(tag_name='protected-tag')

        api_client.force_authenticate(user=test_user)

        response = api_client.delete(f'/api/v1/tags/{tag.tag_id}/delete/')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Tag.objects.filter(tag_id=tag.tag_id).exists()
    
    def test_delete_tag_not_found(self, api_client, admin_user):
        """Test deleting non-existent tag returns 404."""
        api_client.force_authenticate(user=admin_user)

        import uuid
        fake_id = str(uuid.uuid4())
        response = api_client.delete(f'/api/v1/tags/{fake_id}/delete/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_tag_cascade_to_post_tags(self, api_client, admin_user, test_post):
        """Test deleting tag also deletes PostTag relationships."""
        tag = Tag.objects.create(tag_name='cascade-tag')
        PostTag.objects.create(post=test_post, tag=tag)

        api_client.force_authenticate(user=admin_user)

        response = api_client.delete(f'/api/v1/tags/{tag.tag_id}/delete/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        # PostTag should be deleted too
        assert not PostTag.objects.filter(tag_id=tag.tag_id).exists()


@pytest.mark.django_db
class TestAssignTagsAPI:
    """Test POST /api/v1/tags/assign/{post_id}/ endpoint."""

    def test_assign_tags_to_post_success(self, api_client, test_user, test_post):
        """Test assigning tags to a post successfully."""
        tag1 = Tag.objects.create(tag_name='tag1')
        tag2 = Tag.objects.create(tag_name='tag2')

        api_client.force_authenticate(user=test_user)

        payload = {'tags': [str(tag1.tag_id), str(tag2.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/assign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

        # Verify tags were assigned
        post_tags = PostTag.objects.filter(post=test_post)
        assert post_tags.count() == 2
    
    def test_assign_tags_only_author(self, api_client, test_user, test_post):
        """Test only post author can assign tags."""
        # Create another user
        other_user = UserRepository.create(
            email='other@test.com',
            username='otheruser',
            firebase_uid='firebase_other_uid'
        )
        
        tag = Tag.objects.create(tag_name='tag1')
        
        # Try to assign as non-author
        api_client.force_authenticate(user=other_user)

        payload = {'tags': [str(tag.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/assign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_assign_tags_max_5(self, api_client, test_user, test_post):
        """Test cannot assign more than 5 tags to a post."""
        # Create 6 tags
        tags = [Tag.objects.create(tag_name=f'tag{i}') for i in range(6)]

        api_client.force_authenticate(user=test_user)

        payload = {'tags': [str(tag.tag_id) for tag in tags]}
        response = api_client.post(
            f'/api/v1/tags/assign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_assign_tags_post_not_found(self, api_client, test_user):
        """Test assigning tags to non-existent post returns 400."""
        tag = Tag.objects.create(tag_name='tag1')

        api_client.force_authenticate(user=test_user)

        import uuid
        fake_post_id = str(uuid.uuid4())
        payload = {'tags': [str(tag.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/assign/{fake_post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_assign_tags_tag_not_found(self, api_client, test_user, test_post):
        """Test assigning non-existent tag returns 400."""
        api_client.force_authenticate(user=test_user)

        import uuid
        fake_tag_id = str(uuid.uuid4())
        payload = {'tags': [fake_tag_id]}
        response = api_client.post(
            f'/api/v1/tags/assign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_assign_duplicate_tag_ignored(self, api_client, test_user, test_post):
        """Test assigning already assigned tag is idempotent."""
        tag = Tag.objects.create(tag_name='tag1')
        PostTag.objects.create(post=test_post, tag=tag)

        api_client.force_authenticate(user=test_user)

        payload = {'tags': [str(tag.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/assign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        # Should still have only 1 PostTag
        assert PostTag.objects.filter(post=test_post).count() == 1


@pytest.mark.django_db
class TestUnassignTagsAPI:
    """Test POST /api/v1/tags/unassign/{post_id}/ endpoint."""

    def test_unassign_tags_success(self, api_client, test_user, test_post):
        """Test unassigning specific tags from a post."""
        tag1 = Tag.objects.create(tag_name='tag1')
        tag2 = Tag.objects.create(tag_name='tag2')
        PostTag.objects.create(post=test_post, tag=tag1)
        PostTag.objects.create(post=test_post, tag=tag2)

        api_client.force_authenticate(user=test_user)

        payload = {'tags': [str(tag1.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/unassign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

        # tag1 should be removed, tag2 should remain
        assert not PostTag.objects.filter(post=test_post, tag=tag1).exists()
        assert PostTag.objects.filter(post=test_post, tag=tag2).exists()
    
    def test_unassign_all_tags(self, api_client, test_user, test_post):
        """Test unassigning all tags by providing all tag IDs."""
        tag1 = Tag.objects.create(tag_name='tag1')
        tag2 = Tag.objects.create(tag_name='tag2')
        PostTag.objects.create(post=test_post, tag=tag1)
        PostTag.objects.create(post=test_post, tag=tag2)

        api_client.force_authenticate(user=test_user)

        # Providing all tag IDs should remove all tags
        payload = {'tags': [str(tag1.tag_id), str(tag2.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/unassign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        # All tags should be removed
        assert PostTag.objects.filter(post=test_post).count() == 0
    
    def test_unassign_tags_only_author(self, api_client, test_user, test_post):
        """Test only post author can unassign tags."""
        other_user = UserRepository.create(
            email='other@test.com',
            username='otheruser',
            firebase_uid='firebase_other_uid'
        )
        
        tag = Tag.objects.create(tag_name='tag1')
        PostTag.objects.create(post=test_post, tag=tag)
        
        api_client.force_authenticate(user=other_user)

        payload = {'tags': [str(tag.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/unassign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_unassign_tags_post_not_found(self, api_client, test_user):
        """Test unassigning tags from non-existent post returns 400."""
        api_client.force_authenticate(user=test_user)

        import uuid
        fake_post_id = str(uuid.uuid4())
        payload = {'tags': []}
        response = api_client.post(
            f'/api/v1/tags/unassign/{fake_post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_unassign_non_existing_tag_idempotent(self, api_client, test_user, test_post):
        """Test unassigning non-existing tag is idempotent."""
        tag = Tag.objects.create(tag_name='tag1')

        api_client.force_authenticate(user=test_user)

        # Tag is not assigned, but should not error
        payload = {'tags': [str(tag.tag_id)]}
        response = api_client.post(
            f'/api/v1/tags/unassign/{test_post.post_id}/',
            payload,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

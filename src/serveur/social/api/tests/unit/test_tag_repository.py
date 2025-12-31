"""
Unit tests for Tag and PostTag repositories.
Tests data access layer with real database.
"""
import pytest
import uuid
from db.repositories.tag_repository import TagRepository, PostTagRepository
from db.entities.post_entity import Tag, PostTag, Post
from db.entities.user_entity import User, UserProfile, UserSettings


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.objects.create(
        firebase_uid='test-firebase-uid',
        email='test@example.com',
        username='testuser'
    )
    UserProfile.objects.create(user=user)
    UserSettings.objects.create(user=user)
    return user


@pytest.fixture
def test_post(db, test_user):
    """Create a test post."""
    return Post.objects.create(
        user=test_user,
        title='Test Post',
        content='Test content for post'
    )


@pytest.mark.django_db
class TestTagRepository:
    """Test TagRepository operations."""
    
    def test_create_tag_success(self):
        """Test creating a tag successfully."""
        tag = TagRepository.create(tag_name='python', creator_id=None)
        
        assert tag is not None
        assert tag.tag_name == 'python'
        assert tag.creator_id is None
        assert tag.tag_id is not None
    
    def test_create_tag_with_creator(self, test_user):
        """Test creating a tag with a creator."""
        tag = TagRepository.create(
            tag_name='django',
            creator_id=str(test_user.user_id)
        )
        
        assert tag.tag_name == 'django'
        assert str(tag.creator_id) == str(test_user.user_id)
    
    def test_get_by_id_existing(self):
        """Test getting an existing tag by ID."""
        created_tag = TagRepository.create(tag_name='javascript')
        
        retrieved_tag = TagRepository.get_by_id(str(created_tag.tag_id))
        
        assert retrieved_tag is not None
        assert retrieved_tag.tag_id == created_tag.tag_id
        assert retrieved_tag.tag_name == 'javascript'
    
    def test_get_by_id_non_existing(self):
        """Test getting a non-existing tag returns None."""
        fake_id = str(uuid.uuid4())
        
        tag = TagRepository.get_by_id(fake_id)
        
        assert tag is None
    
    def test_get_by_name_existing(self):
        """Test getting an existing tag by name."""
        TagRepository.create(tag_name='react')
        
        tag = TagRepository.get_by_name('react')
        
        assert tag is not None
        assert tag.tag_name == 'react'
    
    def test_get_by_name_non_existing(self):
        """Test getting a non-existing tag by name returns None."""
        tag = TagRepository.get_by_name('nonexistent-tag')
        
        assert tag is None
    
    def test_get_by_name_case_sensitive(self):
        """Test that tag name search is case-sensitive."""
        TagRepository.create(tag_name='Python')
        
        # Exact match should work
        tag_exact = TagRepository.get_by_name('Python')
        assert tag_exact is not None
        
        # Different case should not match
        tag_lower = TagRepository.get_by_name('python')
        assert tag_lower is None
    
    def test_get_all_pagination(self):
        """Test getting all tags with pagination."""
        # Create multiple tags
        for i in range(15):
            TagRepository.create(tag_name=f'tag-{i:02d}')
        
        # Get first page
        page1 = TagRepository.get_all(page=1, page_size=10)
        assert len(page1) == 10
        
        # Get second page
        page2 = TagRepository.get_all(page=2, page_size=10)
        assert len(page2) == 5
    
    def test_get_all_ordering(self):
        """Test that tags are ordered alphabetically."""
        TagRepository.create(tag_name='zebra')
        TagRepository.create(tag_name='apple')
        TagRepository.create(tag_name='mango')
        
        tags = TagRepository.get_all(page=1, page_size=10)
        tag_names = [tag.tag_name for tag in tags]
        
        assert tag_names == sorted(tag_names)
    
    def test_delete_existing_tag(self):
        """Test deleting an existing tag."""
        tag = TagRepository.create(tag_name='to-delete')
        tag_id = str(tag.tag_id)
        
        result = TagRepository.delete(tag_id)
        
        assert result is True
        assert TagRepository.get_by_id(tag_id) is None
    
    def test_delete_non_existing_tag(self):
        """Test deleting a non-existing tag returns False."""
        fake_id = str(uuid.uuid4())
        
        result = TagRepository.delete(fake_id)
        
        assert result is False
    
    def test_tag_unique_constraint(self):
        """Test that tag names must be unique."""
        TagRepository.create(tag_name='unique-tag')
        
        # Attempting to create duplicate should raise error
        with pytest.raises(Exception):  # Django IntegrityError
            TagRepository.create(tag_name='unique-tag')


@pytest.mark.django_db
class TestPostTagRepository:
    """Test PostTagRepository operations."""
    
    def test_create_post_tag_link(self, test_post):
        """Test creating a post-tag link."""
        tag = TagRepository.create(tag_name='test-tag')
        
        post_tag = PostTagRepository.create(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        assert post_tag is not None
        assert str(post_tag.post_id) == str(test_post.post_id)
        assert str(post_tag.tag_id) == str(tag.tag_id)
    
    def test_exists_post_tag_true(self, test_post):
        """Test checking if post-tag link exists."""
        tag = TagRepository.create(tag_name='exists-tag')
        PostTagRepository.create(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        exists = PostTagRepository.exists(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        assert exists is True
    
    def test_exists_post_tag_false(self, test_post):
        """Test checking non-existing post-tag link."""
        tag = TagRepository.create(tag_name='no-link-tag')
        
        exists = PostTagRepository.exists(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        assert exists is False
    
    def test_get_by_post(self, test_post):
        """Test getting all tags for a post."""
        tag1 = TagRepository.create(tag_name='tag1')
        tag2 = TagRepository.create(tag_name='tag2')
        tag3 = TagRepository.create(tag_name='tag3')
        
        PostTagRepository.create(str(test_post.post_id), str(tag1.tag_id))
        PostTagRepository.create(str(test_post.post_id), str(tag2.tag_id))
        PostTagRepository.create(str(test_post.post_id), str(tag3.tag_id))
        
        post_tags = PostTagRepository.get_by_post(str(test_post.post_id))
        
        assert len(list(post_tags)) == 3
        tag_names = [pt.tag.tag_name for pt in post_tags]
        assert 'tag1' in tag_names
        assert 'tag2' in tag_names
        assert 'tag3' in tag_names
    
    def test_get_by_post_empty(self, test_post):
        """Test getting tags for post with no tags."""
        post_tags = PostTagRepository.get_by_post(str(test_post.post_id))
        
        assert len(list(post_tags)) == 0
    
    def test_delete_post_tag(self, test_post):
        """Test deleting a post-tag link."""
        tag = TagRepository.create(tag_name='delete-link-tag')
        PostTagRepository.create(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        result = PostTagRepository.delete(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        assert result is True
        assert not PostTagRepository.exists(
            str(test_post.post_id),
            str(tag.tag_id)
        )
    
    def test_delete_non_existing_post_tag(self, test_post):
        """Test deleting non-existing post-tag link."""
        tag = TagRepository.create(tag_name='no-link')
        
        result = PostTagRepository.delete(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        assert result is False
    
    def test_unique_constraint_post_tag(self, test_post):
        """Test that post-tag combination must be unique."""
        tag = TagRepository.create(tag_name='unique-link')
        PostTagRepository.create(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        # Attempting to create duplicate should raise error
        with pytest.raises(Exception):  # Django IntegrityError
            PostTagRepository.create(
                post_id=str(test_post.post_id),
                tag_id=str(tag.tag_id)
            )
    
    def test_cascade_delete_on_tag_deletion(self, test_post):
        """Test that deleting a tag cascades to PostTag."""
        tag = TagRepository.create(tag_name='cascade-tag')
        PostTagRepository.create(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        # Delete the tag
        TagRepository.delete(str(tag.tag_id))
        
        # PostTag should be deleted too
        exists = PostTagRepository.exists(
            str(test_post.post_id),
            str(tag.tag_id)
        )
        assert exists is False
    
    def test_cascade_delete_on_post_deletion(self, test_post):
        """Test that deleting a post cascades to PostTag."""
        tag = TagRepository.create(tag_name='post-cascade-tag')
        PostTagRepository.create(
            post_id=str(test_post.post_id),
            tag_id=str(tag.tag_id)
        )
        
        post_id = str(test_post.post_id)
        
        # Delete the post
        test_post.delete()
        
        # PostTag should be deleted too
        post_tags = PostTagRepository.get_by_post(post_id)
        assert len(list(post_tags)) == 0

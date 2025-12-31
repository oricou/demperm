"""
Unit tests for TagService.
Tests business logic with mocked dependencies.
"""
import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
from services.apps_services.tag_service import TagService
from common.exceptions import NotFoundError, ValidationError, ConflictError


# Valid UUIDs for tests
TEST_UUID_USER = str(uuid.uuid4())
TEST_UUID_POST = str(uuid.uuid4())
TEST_UUID_TAG_1 = str(uuid.uuid4())
TEST_UUID_TAG_2 = str(uuid.uuid4())


@pytest.mark.django_db
class TestTagServiceGetAllTags:
    """Test TagService.get_all_tags() method."""
    
    @patch('services.apps_services.tag_service.TagRepository')
    def test_get_all_tags_success(self, mock_tag_repo):
        """Test getting all tags successfully."""
        mock_tags = [
            Mock(tag_id=TEST_UUID_TAG_1, tag_name='python'),
            Mock(tag_id=TEST_UUID_TAG_2, tag_name='django')
        ]
        mock_tag_repo.get_all.return_value = mock_tags
        
        result = TagService.get_all_tags(page=1, page_size=100)
        
        assert len(result) == 2
        mock_tag_repo.get_all.assert_called_once_with(1, 100)
    
    @patch('services.apps_services.tag_service.TagRepository')
    def test_get_all_tags_pagination(self, mock_tag_repo):
        """Test pagination parameters are passed correctly."""
        mock_tag_repo.get_all.return_value = []
        
        TagService.get_all_tags(page=3, page_size=50)
        
        mock_tag_repo.get_all.assert_called_once_with(3, 50)
    
    @patch('services.apps_services.tag_service.TagRepository')
    def test_get_all_tags_empty(self, mock_tag_repo):
        """Test getting empty list of tags."""
        mock_tag_repo.get_all.return_value = []
        
        result = TagService.get_all_tags()
        
        assert result == []


@pytest.mark.django_db
class TestTagServiceCreateTag:
    """Test TagService.create_tag() method."""
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.Validator')
    def test_create_tag_success(self, mock_validator, mock_tag_repo, mock_audit):
        """Test creating a tag successfully."""
        mock_validator.validate_tag_name.return_value = 'python'
        mock_tag_repo.get_by_name.return_value = None
        mock_tag_repo.create.return_value = Mock(
            tag_id=TEST_UUID_TAG_1,
            tag_name='python'
        )
        
        result = TagService.create_tag(TEST_UUID_USER, 'python')
        
        assert result is not None
        mock_validator.validate_tag_name.assert_called_once_with('python')
        mock_tag_repo.get_by_name.assert_called_once_with('python')
        mock_tag_repo.create.assert_called_once_with(
            tag_name='python',
            creator_id=TEST_UUID_USER
        )
        mock_audit.create.assert_called_once()
    
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.Validator')
    def test_create_tag_duplicate(self, mock_validator, mock_tag_repo):
        """Test creating duplicate tag raises ConflictError."""
        mock_validator.validate_tag_name.return_value = 'python'
        mock_tag_repo.get_by_name.return_value = Mock(tag_name='python')
        
        with pytest.raises(ConflictError, match="Tag already exists"):
            TagService.create_tag(TEST_UUID_USER, 'python')
    
    @patch('services.apps_services.tag_service.Validator')
    def test_create_tag_invalid_name(self, mock_validator):
        """Test creating tag with invalid name raises ValidationError."""
        mock_validator.validate_tag_name.side_effect = ValidationError("Invalid tag name")
        
        with pytest.raises(ValidationError, match="Invalid tag name"):
            TagService.create_tag(TEST_UUID_USER, 'invalid tag!')
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.Validator')
    def test_create_tag_audit_log_created(self, mock_validator, mock_tag_repo, mock_audit):
        """Test that audit log is created when tag is created."""
        mock_validator.validate_tag_name.return_value = 'django'
        mock_tag_repo.get_by_name.return_value = None
        mock_tag_repo.create.return_value = Mock(tag_id=TEST_UUID_TAG_1)
        
        TagService.create_tag(TEST_UUID_USER, 'django')
        
        call_args = mock_audit.create.call_args
        assert call_args[1]['user_id'] == TEST_UUID_USER
        assert call_args[1]['action_type'] == 'tag_created'
        assert call_args[1]['resource_type'] == 'tag'
        assert call_args[1]['resource_id'] == str(TEST_UUID_TAG_1)
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.Validator')
    def test_create_tag_empty_name(self, mock_validator, mock_tag_repo, mock_audit):
        """Test creating tag with empty name raises ValidationError."""
        mock_validator.validate_tag_name.side_effect = ValidationError("Tag name cannot be empty")
        
        with pytest.raises(ValidationError, match="Tag name cannot be empty"):
            TagService.create_tag(TEST_UUID_USER, '')


@pytest.mark.django_db
class TestTagServiceAssignTags:
    """Test TagService.assign_tags_to_post() method."""
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_assign_tags_success(self, mock_post_repo, mock_tag_repo, 
                                 mock_post_tag_repo, mock_audit):
        """Test assigning tags to a post successfully."""
        # Setup mocks
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        mock_tag = Mock(tag_id=TEST_UUID_TAG_1)
        mock_tag_repo.get_by_id.return_value = mock_tag
        
        mock_post_tag_repo.get_by_post.return_value = []
        mock_post_tag_repo.exists.return_value = False
        
        # Execute
        TagService.assign_tags_to_post(
            TEST_UUID_USER,
            TEST_UUID_POST,
            [TEST_UUID_TAG_1]
        )
        
        # Verify
        mock_post_repo.get_by_id.assert_called_once_with(TEST_UUID_POST)
        mock_tag_repo.get_by_id.assert_called_once_with(TEST_UUID_TAG_1)
        mock_post_tag_repo.create.assert_called_once_with(
            TEST_UUID_POST,
            TEST_UUID_TAG_1
        )
        mock_audit.create.assert_called_once()
    
    @patch('services.apps_services.tag_service.PostRepository')
    def test_assign_tags_post_not_found(self, mock_post_repo):
        """Test assigning tags to non-existent post raises NotFoundError."""
        mock_post_repo.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError, match="Post .* not found"):
            TagService.assign_tags_to_post(
                TEST_UUID_USER,
                TEST_UUID_POST,
                [TEST_UUID_TAG_1]
            )
    
    @patch('services.apps_services.tag_service.PostRepository')
    def test_assign_tags_not_author(self, mock_post_repo):
        """Test non-author cannot assign tags."""
        mock_post = Mock()
        mock_post.user = Mock(user_id='different-user-id')
        mock_post_repo.get_by_id.return_value = mock_post
        
        with pytest.raises(ValidationError, match="Only the author can assign tags"):
            TagService.assign_tags_to_post(
                TEST_UUID_USER,
                TEST_UUID_POST,
                [TEST_UUID_TAG_1]
            )
    
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_assign_tags_max_limit(self, mock_post_repo, mock_post_tag_repo):
        """Test cannot assign more than 5 tags to a post."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        # Mock 5 existing tags
        existing_tags = [Mock() for _ in range(5)]
        mock_post_tag_repo.get_by_post.return_value = existing_tags
        
        with pytest.raises(ValidationError, match="cannot have more than 5 tags"):
            TagService.assign_tags_to_post(
                TEST_UUID_USER,
                TEST_UUID_POST,
                [TEST_UUID_TAG_1]
            )
    
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_assign_tags_tag_not_found(self, mock_post_repo, mock_post_tag_repo, 
                                       mock_tag_repo):
        """Test assigning non-existent tag raises NotFoundError."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        mock_post_tag_repo.get_by_post.return_value = []
        mock_tag_repo.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError, match="Tag .* not found"):
            TagService.assign_tags_to_post(
                TEST_UUID_USER,
                TEST_UUID_POST,
                [TEST_UUID_TAG_1]
            )
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_assign_tags_duplicate_ignored(self, mock_post_repo, mock_tag_repo,
                                           mock_post_tag_repo, mock_audit):
        """Test assigning already assigned tag is skipped."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        mock_tag = Mock(tag_id=TEST_UUID_TAG_1)
        mock_tag_repo.get_by_id.return_value = mock_tag
        
        mock_post_tag_repo.get_by_post.return_value = []
        mock_post_tag_repo.exists.return_value = True  # Already exists
        
        TagService.assign_tags_to_post(
            TEST_UUID_USER,
            TEST_UUID_POST,
            [TEST_UUID_TAG_1]
        )
        
        # Should not create duplicate
        mock_post_tag_repo.create.assert_not_called()
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.TagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_assign_multiple_tags(self, mock_post_repo, mock_tag_repo,
                                  mock_post_tag_repo, mock_audit):
        """Test assigning multiple tags at once."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        mock_tag_repo.get_by_id.return_value = Mock()
        mock_post_tag_repo.get_by_post.return_value = []
        mock_post_tag_repo.exists.return_value = False
        
        tag_ids = [str(uuid.uuid4()) for _ in range(3)]
        
        TagService.assign_tags_to_post(
            TEST_UUID_USER,
            TEST_UUID_POST,
            tag_ids
        )
        
        assert mock_post_tag_repo.create.call_count == 3


@pytest.mark.django_db
class TestTagServiceUnassignTags:
    """Test TagService.unassign_tags_from_post() method."""
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_unassign_tags_success(self, mock_post_repo, mock_post_tag_repo, mock_audit):
        """Test unassigning specific tags from a post."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        TagService.unassign_tags_from_post(
            TEST_UUID_USER,
            TEST_UUID_POST,
            [TEST_UUID_TAG_1]
        )
        
        mock_post_tag_repo.delete.assert_called_once_with(
            TEST_UUID_POST,
            TEST_UUID_TAG_1
        )
        mock_audit.create.assert_called_once()
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_unassign_all_tags(self, mock_post_repo, mock_post_tag_repo, mock_audit):
        """Test unassigning all tags when tag_ids is None."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        # Mock existing tags
        mock_post_tags = [
            Mock(tag=Mock(tag_id=TEST_UUID_TAG_1)),
            Mock(tag=Mock(tag_id=TEST_UUID_TAG_2))
        ]
        mock_post_tag_repo.get_by_post.return_value = mock_post_tags
        
        TagService.unassign_tags_from_post(
            TEST_UUID_USER,
            TEST_UUID_POST,
            tag_ids=None
        )
        
        assert mock_post_tag_repo.delete.call_count == 2
    
    @patch('services.apps_services.tag_service.PostRepository')
    def test_unassign_tags_post_not_found(self, mock_post_repo):
        """Test unassigning tags from non-existent post raises NotFoundError."""
        mock_post_repo.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError, match="Post .* not found"):
            TagService.unassign_tags_from_post(
                TEST_UUID_USER,
                TEST_UUID_POST,
                [TEST_UUID_TAG_1]
            )
    
    @patch('services.apps_services.tag_service.PostRepository')
    def test_unassign_tags_not_author(self, mock_post_repo):
        """Test non-author cannot unassign tags."""
        mock_post = Mock()
        mock_post.user = Mock(user_id='different-user-id')
        mock_post_repo.get_by_id.return_value = mock_post
        
        with pytest.raises(ValidationError, match="Only the author can unassign tags"):
            TagService.unassign_tags_from_post(
                TEST_UUID_USER,
                TEST_UUID_POST,
                [TEST_UUID_TAG_1]
            )
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_unassign_tags_audit_log(self, mock_post_repo, mock_post_tag_repo, mock_audit):
        """Test that audit log is created when unassigning tags."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        tag_ids = [TEST_UUID_TAG_1, TEST_UUID_TAG_2]
        
        TagService.unassign_tags_from_post(
            TEST_UUID_USER,
            TEST_UUID_POST,
            tag_ids
        )
        
        call_args = mock_audit.create.call_args
        assert call_args[1]['user_id'] == TEST_UUID_USER
        assert call_args[1]['action_type'] == 'tags_unassigned'
        assert call_args[1]['resource_type'] == 'post'
        assert call_args[1]['resource_id'] == TEST_UUID_POST
        assert call_args[1]['details']['tags'] == tag_ids
    
    @patch('services.apps_services.tag_service.AuditLogRepository')
    @patch('services.apps_services.tag_service.PostTagRepository')
    @patch('services.apps_services.tag_service.PostRepository')
    def test_unassign_non_existing_tag_idempotent(self, mock_post_repo, 
                                                   mock_post_tag_repo, mock_audit):
        """Test unassigning non-existing tag is idempotent."""
        mock_post = Mock()
        mock_post.user = Mock(user_id=TEST_UUID_USER)
        mock_post_repo.get_by_id.return_value = mock_post
        
        # delete returns False for non-existing
        mock_post_tag_repo.delete.return_value = False
        
        # Should not raise error
        TagService.unassign_tags_from_post(
            TEST_UUID_USER,
            TEST_UUID_POST,
            [TEST_UUID_TAG_1]
        )
        
        mock_post_tag_repo.delete.assert_called_once()

"""
Unit tests for validators.
"""
import pytest
from common.validators import Validator
from common.exceptions import ValidationError


@pytest.mark.unit
class TestValidator:
    """Test Validator class."""
    
    def test_validate_username_valid(self):
        """Test valid username."""
        username = Validator.validate_username('testuser123')
        assert username == 'testuser123'
    
    def test_validate_username_too_short(self):
        """Test username too short."""
        with pytest.raises(ValidationError) as exc:
            Validator.validate_username('ab')
        assert 'must be 3-50 characters' in str(exc.value)
    
    def test_validate_username_too_long(self):
        """Test username too long."""
        with pytest.raises(ValidationError) as exc:
            Validator.validate_username('a' * 51)
        assert 'must be 3-50 characters' in str(exc.value)
    
    def test_validate_username_invalid_chars(self):
        """Test username with invalid characters."""
        with pytest.raises(ValidationError) as exc:
            Validator.validate_username('test@user')
        assert 'can only contain' in str(exc.value)
    
    def test_validate_email_valid(self):
        """Test valid email."""
        email = Validator.validate_email('test@example.com')
        assert email == 'test@example.com'
    
    def test_validate_email_invalid(self):
        """Test invalid email."""
        with pytest.raises(ValidationError) as exc:
            Validator.validate_email('invalid-email')
        assert 'Invalid email format' in str(exc.value)
    
    def test_validate_post_title_valid(self):
        """Test valid post title."""
        title = Validator.validate_post_title('This is a valid title')
        assert title == 'This is a valid title'
    
    def test_validate_post_title_too_long(self):
        """Test post title too long."""
        with pytest.raises(ValidationError) as exc:
            Validator.validate_post_title('a' * 201)
        assert 'must be 1-200 characters' in str(exc.value)
    
    def test_validate_tag_name_valid(self):
        """Test valid tag name."""
        tag = Validator.validate_tag_name('politics')
        assert tag == 'politics'
    
    def test_validate_tag_name_lowercase(self):
        """Test tag name is converted to lowercase."""
        tag = Validator.validate_tag_name('POLITICS')
        assert tag == 'politics'


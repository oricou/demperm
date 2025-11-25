"""
Input validators and sanitizers.
"""
import re
import bleach
from typing import Optional
from common.exceptions import ValidationError


class Validator:
    """Input validation utilities."""
    
    @staticmethod
    def validate_username(username: str) -> str:
        """Validate username format."""
        if not username:
            raise ValidationError("Username is required")
        
        if len(username) < 3 or len(username) > 50:
            raise ValidationError("Username must be 3-50 characters")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, _ and -")
        
        return username
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email format."""
        if not email:
            raise ValidationError("Email is required")
        
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Invalid email format")
        
        return email.lower()
    
    @staticmethod
    def validate_post_title(title: str) -> str:
        """Validate post title."""
        if not title:
            raise ValidationError("Title is required")
        
        if len(title) < 1 or len(title) > 200:
            raise ValidationError("Title must be 1-200 characters")
        
        if not re.match(r'^[a-zA-Z0-9 .,!?\'À-ÿ-]+$', title):
            raise ValidationError("Title contains invalid characters")
        
        return title.strip()
    
    @staticmethod
    def validate_post_content(content: str) -> str:
        """Validate and sanitize post content."""
        if not content:
            raise ValidationError("Content is required")
        
        if len(content) < 1 or len(content) > 10000:
            raise ValidationError("Content must be 1-10000 characters")
        
        # Sanitize HTML
        return Sanitizer.sanitize_html(content)
    
    @staticmethod
    def validate_comment_content(content: str) -> str:
        """Validate and sanitize comment content."""
        if not content:
            raise ValidationError("Content is required")
        
        if len(content) < 1 or len(content) > 2000:
            raise ValidationError("Content must be 1-2000 characters")
        
        # Sanitize HTML
        return Sanitizer.sanitize_html(content)
    
    @staticmethod
    def validate_bio(bio: Optional[str]) -> Optional[str]:
        """Validate bio."""
        if bio is None:
            return None
        
        if len(bio) > 500:
            raise ValidationError("Bio must be max 500 characters")
        
        return Sanitizer.sanitize_html(bio)
    
    @staticmethod
    def validate_tag_name(tag_name: str) -> str:
        """Validate tag name."""
        if not tag_name:
            raise ValidationError("Tag name is required")
        
        if len(tag_name) < 2 or len(tag_name) > 50:
            raise ValidationError("Tag name must be 2-50 characters")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', tag_name):
            raise ValidationError("Tag name can only contain letters, numbers, _ and -")
        
        return tag_name.lower()
    
    @staticmethod
    def validate_forum_name(forum_name: str) -> str:
        """Validate forum name."""
        if not forum_name:
            raise ValidationError("Forum name is required")
        
        if len(forum_name) < 3 or len(forum_name) > 200:
            raise ValidationError("Forum name must be 3-200 characters")
        
        return forum_name.strip()
    
    @staticmethod
    def validate_description(description: Optional[str], max_length: int = 1000) -> Optional[str]:
        """Validate description."""
        if description is None:
            return None
        
        if len(description) > max_length:
            raise ValidationError(f"Description must be max {max_length} characters")
        
        return Sanitizer.sanitize_html(description)


class Sanitizer:
    """HTML sanitization utilities."""
    
    # Allowed HTML tags
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'blockquote', 'code', 'pre'
    ]
    
    # Allowed attributes
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title'],
    }
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """Sanitize HTML content using bleach."""
        return bleach.clean(
            content,
            tags=Sanitizer.ALLOWED_TAGS,
            attributes=Sanitizer.ALLOWED_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def strip_html(content: str) -> str:
        """Strip all HTML tags."""
        return bleach.clean(content, tags=[], strip=True)


"""
Common utility functions.
"""
import hashlib
import hmac
import secrets
from typing import Optional
from django.conf import settings


def generate_content_signature(content: str) -> str:
    """
    Generate HMAC-SHA256 signature for content integrity.
    
    Args:
        content: Content to sign
        
    Returns:
        Hex-encoded signature
    """
    secret_key = settings.SECRET_KEY.encode('utf-8')
    content_bytes = content.encode('utf-8')
    signature = hmac.new(secret_key, content_bytes, hashlib.sha256)
    return signature.hexdigest()


def verify_content_signature(content: str, signature: str) -> bool:
    """
    Verify content signature.
    
    Args:
        content: Content to verify
        signature: Signature to check
        
    Returns:
        True if signature is valid
    """
    expected_signature = generate_content_signature(content)
    return hmac.compare_digest(expected_signature, signature)


def generate_random_state(length: int = 32) -> str:
    """
    Generate random state for OAuth2 CSRF protection.
    
    Args:
        length: Length of the state string
        
    Returns:
        Random hex string
    """
    return secrets.token_hex(length)


def get_client_ip(request) -> Optional[str]:
    """
    Get client IP address from request.
    
    Args:
        request: Django request object
        
    Returns:
        IP address string
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def paginate_queryset(queryset, page: int = 1, page_size: int = 20):
    """
    Paginate a queryset.
    
    Args:
        queryset: Django queryset
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Tuple of (paginated_items, pagination_info)
    """
    # Ensure page and page_size are valid
    page = max(1, page)
    page_size = min(max(1, page_size), 100)  # Max 100 items per page
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get total count
    total = queryset.count()
    
    # Get paginated items
    items = list(queryset[offset:offset + page_size])
    
    # Calculate pagination info
    total_pages = (total + page_size - 1) // page_size
    has_next = page < total_pages
    has_previous = page > 1
    
    pagination_info = {
        'page': page,
        'page_size': page_size,
        'total': total,
        'total_pages': total_pages,
        'has_next': has_next,
        'has_previous': has_previous,
    }
    
    return items, pagination_info


def build_pagination_response(items: list, pagination_info: dict, item_serializer=None):
    """
    Build a paginated response.
    
    Args:
        items: List of items
        pagination_info: Pagination metadata
        item_serializer: Optional serializer function for items
        
    Returns:
        Response dictionary
    """
    if item_serializer:
        items = [item_serializer(item) for item in items]
    
    return {
        'results': items,
        'pagination': pagination_info,
    }


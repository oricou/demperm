"""
Rate limiting decorators and utilities.
"""
from functools import wraps
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


def rate_limit(key_prefix: str, limit: int, period: int):
    """
    Rate limiting decorator.
    
    Args:
        key_prefix: Prefix for the cache key
        limit: Maximum number of requests
        period: Time period in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Skip rate limiting if disabled
            if not getattr(settings, 'RATE_LIMIT_ENABLED', True):
                return func(self, request, *args, **kwargs)
            
            # Get user identifier
            if request.user and request.user.is_authenticated:
                user_id = str(request.user.user_id)
            else:
                # Use IP address for anonymous users
                user_id = get_client_ip(request)
            
            # Create cache key
            cache_key = f"rate_limit:{key_prefix}:{user_id}"
            
            # Get current count
            current_count = cache.get(cache_key, 0)
            
            # Check if limit exceeded
            if current_count >= limit:
                return Response(
                    {
                        'error': {
                            'code': 'RATE_LIMIT_EXCEEDED',
                            'message': f'Rate limit exceeded. Try again in {period} seconds.',
                        }
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            # Increment counter
            cache.set(cache_key, current_count + 1, period)
            
            # Call the original function
            return func(self, request, *args, **kwargs)
        
        return wrapper
    return decorator


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Predefined rate limiters
def rate_limit_auth(func):
    """Rate limit for authentication endpoints: 10 requests per minute."""
    return rate_limit('auth', 10, 60)(func)


def rate_limit_post_create(func):
    """Rate limit for post creation: 10 requests per hour."""
    return rate_limit('post_create', 10, 3600)(func)


def rate_limit_comment_create(func):
    """Rate limit for comment creation: 30 requests per hour."""
    return rate_limit('comment_create', 30, 3600)(func)


def rate_limit_like(func):
    """Rate limit for likes: 100 requests per hour."""
    return rate_limit('like', 100, 3600)(func)


def rate_limit_message_send(func):
    """Rate limit for sending messages: 50 requests per hour."""
    return rate_limit('message_send', 50, 3600)(func)


def rate_limit_report(func):
    """Rate limit for reports: 20 requests per hour."""
    return rate_limit('report', 20, 3600)(func)


def rate_limit_search(func):
    """Rate limit for search: 100 requests per hour."""
    return rate_limit('search', 100, 3600)(func)


def rate_limit_profile_update(func):
    """Rate limit for profile updates: 10 requests per hour."""
    return rate_limit('profile_update', 10, 3600)(func)


def rate_limit_block(func):
    """Rate limit for blocking users: 20 requests per hour."""
    return rate_limit('block', 20, 3600)(func)


def rate_limit_general(func):
    """General rate limit: 100 requests per hour."""
    return rate_limit('general', 100, 3600)(func)


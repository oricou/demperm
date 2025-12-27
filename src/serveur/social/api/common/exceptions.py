"""
Custom exceptions and exception handler.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging


class BaseAPIException(Exception):
    """Base exception for API errors."""
    
    def __init__(self, message: str, code: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(BaseAPIException):
    """Validation error."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, 'VALIDATION_ERROR', status.HTTP_400_BAD_REQUEST)
        self.details = details or {}


class AuthenticationError(BaseAPIException):
    """Authentication error."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 'AUTHENTICATION_ERROR', status.HTTP_401_UNAUTHORIZED)


class PermissionDeniedError(BaseAPIException):
    """Permission denied error."""
    
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, 'PERMISSION_DENIED', status.HTTP_403_FORBIDDEN)


class NotFoundError(BaseAPIException):
    """Resource not found error."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 'NOT_FOUND', status.HTTP_404_NOT_FOUND)


class ConflictError(BaseAPIException):
    """Conflict error (e.g., duplicate resource)."""
    
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, 'CONFLICT', status.HTTP_409_CONFLICT)


class RateLimitError(BaseAPIException):
    """Rate limit exceeded error."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, 'RATE_LIMIT_EXCEEDED', status.HTTP_429_TOO_MANY_REQUESTS)


class UserBannedError(BaseAPIException):
    """User is banned error."""
    
    def __init__(self, message: str = "User is banned"):
        super().__init__(message, 'USER_BANNED', status.HTTP_403_FORBIDDEN)


class UserBlockedError(BaseAPIException):
    """User is blocked error."""
    
    def __init__(self, message: str = "User is blocked"):
        super().__init__(message, 'USER_BLOCKED', status.HTTP_403_FORBIDDEN)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Handle custom exceptions
    if isinstance(exc, BaseAPIException):
        error_response = {
            'error': {
                'code': exc.code,
                'message': exc.message,
            }
        }
        
        # Add details for validation errors
        if isinstance(exc, ValidationError) and exc.details:
            error_response['error']['details'] = exc.details
        
        return Response(error_response, status=exc.status_code)
    
    # If response is None, it's not a DRF exception
    if response is None:
        # Log the unexpected exception with full traceback so it's visible
        # in server logs during tests and debugging.
        logging.getLogger('django').exception('Unhandled exception in request')

        # Handle unexpected errors (keep generic response to clients)
        return Response(
            {
                'error': {
                    'code': 'INTERNAL_SERVER_ERROR',
                    'message': 'An unexpected error occurred',
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Format DRF exceptions to match our error format
    error_response = {
        'error': {
            'code': 'API_ERROR',
            'message': str(response.data.get('detail', 'An error occurred')),
        }
    }
    
    # Add field-specific errors if present
    if isinstance(response.data, dict) and 'detail' not in response.data:
        error_response['error']['details'] = response.data
    
    return Response(error_response, status=response.status_code)


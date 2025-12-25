"""
Helpers for standardized API responses in admin_panel.
"""
import uuid
from django.utils import timezone
from rest_framework.response import Response


def _meta():
    return {
        'timestamp': timezone.now().isoformat(),
        'request_id': str(uuid.uuid4()),
    }


def api_success(data=None, pagination=None, status_code=200):
    """
    Build a success response with meta block.
    """
    if status_code == 204:
        return Response(status=status_code)
    body = {'meta': _meta()}
    if data is not None:
        body['data'] = data
    if pagination is not None:
        body['pagination'] = pagination
    return Response(body, status=status_code)


def api_error(code: str, message: str, details=None, status_code: int = 400):
    """
    Build an error response following the standard format.
    """
    body = {
        'error': {
            'code': code,
            'message': message,
        },
        'meta': _meta()
    }
    if details is not None:
        body['error']['details'] = details
    return Response(body, status=status_code)

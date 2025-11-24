from typing import Optional, Tuple

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.backends import TokenBackend

from db.entities.user_entity import User


class _WrappedUser:
    """Light wrapper to present a Django-like user to the rest framework.

    It delegates attribute access to the underlying db.User instance and
    exposes `is_authenticated` as True so permission checks work.
    """
    def __init__(self, user: User):
        self._user = user

    @property
    def is_authenticated(self) -> bool:  # type: ignore[override]
        return True

    def __getattr__(self, item):
        return getattr(self._user, item)


class CustomJWTAuthentication(BaseAuthentication):
    """Authenticate requests through a Bearer JWT and map to db.User.

    This avoids relying on Django's auth.User model. Tokens are decoded and
    validated using SimpleJWT's TokenBackend. The token must contain the
    user id under the claim configured in SIMPLE_JWT['USER_ID_CLAIM'] (default
    'user_id').
    """

    www_authenticate_realm = 'api'

    def authenticate(self, request) -> Optional[Tuple[_WrappedUser, str]]:
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2:
            return None

        scheme, token = parts[0], parts[1]
        if scheme.lower() != 'bearer':
            return None

        try:
            token_backend = TokenBackend(
                algorithm=settings.SIMPLE_JWT.get('ALGORITHM', 'HS256'),
                signing_key=settings.SIMPLE_JWT.get('SIGNING_KEY'),
            )
            validated = token_backend.decode(token, verify=True)
        except Exception as exc:  # token invalid / expired / wrong signature
            raise exceptions.AuthenticationFailed('Invalid or expired token') from exc

        user_id_claim = settings.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')
        user_id = validated.get(user_id_claim)
        if not user_id:
            raise exceptions.AuthenticationFailed('Token contained no recognizable user id')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (_WrappedUser(user), token)

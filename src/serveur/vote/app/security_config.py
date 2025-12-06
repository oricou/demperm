from typing import Optional, Tuple
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

from drf_spectacular.extensions import OpenApiAuthenticationExtension

class FirebaseUser:
    """Minimal user object holding only the Firebase UID."""
    
    def __init__(self, uid: str):
        self.id = uid

    @property
    def is_authenticated(self) -> bool:
        return True


class FirebaseAuthentication(BaseAuthentication):

    def authenticate(self, request) -> Optional[Tuple[FirebaseUser, str]]:

        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2:
            return None

        scheme, token = parts
        if scheme.lower() != 'bearer':
            return None

        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred)

        try:
            decoded = firebase_auth.verify_id_token(token)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid or expired Firebase token")

        uid = decoded.get("uid")
        if not uid:
            raise exceptions.AuthenticationFailed("Firebase token missing UID")

        # Keep UID in request if needed
        request.firebase_uid = uid

        user = FirebaseUser(uid=uid)
        return (user, token)

from typing import Optional, Tuple

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

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


class FirebaseAuthentication(BaseAuthentication):
    """Authenticate requests through Firebase JWT tokens.
    
    Verifies Firebase ID tokens from the frontend and maps them to db.User.
    If the token is valid but no user exists in the database, returns None
    with the Firebase UID stored in request for later user creation.
    """

    www_authenticate_realm = 'api'

    def authenticate(self, request) -> Optional[Tuple[Optional[_WrappedUser], str]]:
        """
        Authenticate the request using Firebase JWT token.
        
        Returns:
            - (_WrappedUser, token) if user exists in database
            - None if no Authorization header
            
        Raises:
            AuthenticationFailed: If token is invalid or expired
        """
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2:
            return None

        scheme, token = parts[0], parts[1]
        if scheme.lower() != 'bearer':
            return None

        # Initialize Firebase Admin SDK if not already done
        if not firebase_admin._apps:
            cred_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_KEY', None)
            if cred_path:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                # Initialize with default credentials (for Cloud environments)
                firebase_admin.initialize_app()

        try:
            # Verify the Firebase ID token
            decoded_token = firebase_auth.verify_id_token(token)
            firebase_uid = decoded_token.get('uid')
            
            if not firebase_uid:
                raise exceptions.AuthenticationFailed('Token contained no user ID')
            
            # Store Firebase info in request for later use (user creation)
            request.firebase_uid = firebase_uid
            request.firebase_email = decoded_token.get('email')
            request.firebase_token = decoded_token
            
            # Try to find user in database by firebase_uid
            # Assuming User model has a firebase_uid field (needs to be added)
            try:
                user = User.objects.get(firebase_uid=firebase_uid)
                return (_WrappedUser(user), token)
            except User.DoesNotExist:
                # User authenticated via Firebase but not in database yet
                # Return None to allow endpoint to handle user creation
                return None
                
        except firebase_auth.InvalidIdTokenError as exc:
            print(f"Firebase InvalidIdTokenError: {exc}")
            raise exceptions.AuthenticationFailed('Invalid Firebase token') from exc
        except firebase_auth.ExpiredIdTokenError as exc:
            print(f"Firebase ExpiredIdTokenError: {exc}")
            raise exceptions.AuthenticationFailed('Firebase token expired') from exc
        except Exception as exc:
            print(f"Firebase authentication exception: {type(exc).__name__}: {exc}")
            import traceback
            traceback.print_exc()
            raise exceptions.AuthenticationFailed('Firebase authentication failed') from exc

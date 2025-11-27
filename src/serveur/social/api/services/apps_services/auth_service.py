"""
Authentication service for Google OAuth2 and JWT token management.
"""
import requests
from typing import Optional, Dict
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from db.repositories.user_repository import UserRepository
from db.repositories.message_repository import AuditLogRepository
from db.entities.user_entity import User, UserProfile, UserSettings
from common.exceptions import AuthenticationError
from common.utils import generate_random_state


class AuthService:
    """Service for authentication operations."""
    
    GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
    GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
    GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
    
    @staticmethod
    def get_google_auth_url(redirect_uri: str) -> Dict[str, str]:
        """
        Generate Google OAuth2 authorization URL.
        
        Args:
            redirect_uri: Callback URL
            
        Returns:
            Dictionary with auth_url and state
        """
        state = generate_random_state()
        
        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'access_type': 'offline',
            'prompt': 'consent',
        }
        
        auth_url = f"{AuthService.GOOGLE_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        
        return {
            'auth_url': auth_url,
            'state': state,
        }
    
    @staticmethod
    def exchange_code_for_token(code: str, redirect_uri: str) -> str:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from Google
            redirect_uri: Callback URL
            
        Returns:
            Access token
        """
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        
        response = requests.post(AuthService.GOOGLE_TOKEN_URL, data=data)
        
        if response.status_code != 200:
            raise AuthenticationError('Failed to exchange code for token')
        
        token_data = response.json()
        return token_data.get('access_token')
    
    @staticmethod
    def get_google_user_info(access_token: str) -> Dict:
        """
        Get user info from Google.
        
        Args:
            access_token: Google access token
            
        Returns:
            User info dictionary
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(AuthService.GOOGLE_USERINFO_URL, headers=headers)
        
        if response.status_code != 200:
            raise AuthenticationError('Failed to get user info from Google')
        
        return response.json()
    
    @staticmethod
    def authenticate_with_google(code: str, redirect_uri: str, ip_address: Optional[str] = None) -> Dict:
        """
        Authenticate user with Google OAuth2.
        
        Args:
            code: Authorization code
            redirect_uri: Callback URL
            ip_address: Client IP address for audit log
            
        Returns:
            Dictionary with user and tokens
        """
        # Exchange code for token
        access_token = AuthService.exchange_code_for_token(code, redirect_uri)
        
        # Get user info
        user_info = AuthService.get_google_user_info(access_token)
        
        google_id = user_info.get('id')
        email = user_info.get('email')
        
        if not google_id or not email:
            raise AuthenticationError('Invalid user info from Google')
        
        # Get or create user
        user = UserRepository.get_by_google_id(google_id)
        
        if not user:
            # Create new user
            username = email.split('@')[0]  # Default username from email
            user = UserRepository.create(
                google_id=google_id,
                email=email,
                username=username
            )
            
            # Create profile and settings
            UserProfile.objects.create(
                user=user,
                display_name=user_info.get('name', username)
            )
            UserSettings.objects.create(user=user)
            
            # Log user creation
            AuditLogRepository.create(
                user_id=str(user.user_id),
                action_type='user_created',
                resource_type='user',
                resource_id=str(user.user_id),
                ip_address=ip_address
            )
        else:
            # Log login
            AuditLogRepository.create(
                user_id=str(user.user_id),
                action_type='user_login',
                resource_type='user',
                resource_id=str(user.user_id),
                ip_address=ip_address
            )
        
        # Generate JWT tokens
        tokens = AuthService.generate_tokens(user)
        
        return {
            'user': user,
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh'],
        }
    
    @staticmethod
    def generate_tokens(user: User) -> Dict[str, str]:
        """
        Generate JWT access and refresh tokens.
        
        Args:
            user: User instance
            
        Returns:
            Dictionary with access and refresh tokens
        """
        refresh = RefreshToken.for_user(user)
        
        # Add custom claims
        refresh['user_id'] = str(user.user_id)
        refresh['email'] = user.email
        refresh['is_admin'] = user.is_admin
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


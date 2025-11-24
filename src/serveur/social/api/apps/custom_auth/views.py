"""
Authentication views for Google OAuth2 and JWT.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.auth_service import AuthService
from common.rate_limiters import rate_limit_auth
from common.utils import get_client_ip
from common.exceptions import AuthenticationError
from .serializers import (
    GoogleAuthURLSerializer,
    GoogleAuthCallbackSerializer,
    TokenRefreshSerializer,
    AuthResponseSerializer,
    TokenResponseSerializer,
    UserSerializer,
)


class GoogleAuthURLView(APIView):
    """Get Google OAuth2 authorization URL."""
    
    @swagger_auto_schema(
        operation_description="Get Google OAuth2 authorization URL",
        request_body=GoogleAuthURLSerializer,
        responses={
            200: openapi.Response(
                description="Authorization URL",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'auth_url': openapi.Schema(type=openapi.TYPE_STRING),
                        'state': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        }
    )
    @rate_limit_auth
    def post(self, request):
        """Get Google auth URL."""
        serializer = GoogleAuthURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        redirect_uri = serializer.validated_data['redirect_uri']
        result = AuthService.get_google_auth_url(redirect_uri)
        
        return Response(result, status=status.HTTP_200_OK)


class GoogleAuthCallbackView(APIView):
    """Handle Google OAuth2 callback."""
    
    @swagger_auto_schema(
        operation_description="Handle Google OAuth2 callback and authenticate user",
        request_body=GoogleAuthCallbackSerializer,
        responses={
            200: AuthResponseSerializer,
            401: "Authentication failed"
        }
    )
    @rate_limit_auth
    def post(self, request):
        """Handle Google callback."""
        serializer = GoogleAuthCallbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        redirect_uri = serializer.validated_data['redirect_uri']
        ip_address = get_client_ip(request)
        
        try:
            result = AuthService.authenticate_with_google(code, redirect_uri, ip_address)
            
            # Serialize user
            user_data = UserSerializer(result['user']).data
            
            response_data = {
                'user': user_data,
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except AuthenticationError as e:
            return Response(
                {'error': {'code': 'AUTHENTICATION_ERROR', 'message': str(e)}},
                status=status.HTTP_401_UNAUTHORIZED
            )


class TokenRefreshView(APIView):
    """Refresh JWT access token."""
    
    @swagger_auto_schema(
        operation_description="Refresh JWT access token",
        request_body=TokenRefreshSerializer,
        responses={
            200: TokenResponseSerializer,
            401: "Invalid refresh token"
        }
    )
    @rate_limit_auth
    def post(self, request):
        """Refresh access token."""
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            refresh = RefreshToken(serializer.validated_data['refresh'])
            access_token = str(refresh.access_token)
            
            return Response(
                {'access_token': access_token},
                status=status.HTTP_200_OK
            )
        
        except TokenError:
            return Response(
                {'error': {'code': 'INVALID_TOKEN', 'message': 'Invalid refresh token'}},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """Logout user (blacklist refresh token)."""
    
    @swagger_auto_schema(
        operation_description="Logout user and blacklist refresh token",
        request_body=TokenRefreshSerializer,
        responses={
            200: "Logged out successfully",
            400: "Invalid token"
        }
    )
    def post(self, request):
        """Logout user."""
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            refresh = RefreshToken(serializer.validated_data['refresh'])
            refresh.blacklist()
            
            return Response(
                {'message': 'Logged out successfully'},
                status=status.HTTP_200_OK
            )
        
        except TokenError:
            return Response(
                {'error': {'code': 'INVALID_TOKEN', 'message': 'Invalid refresh token'}},
                status=status.HTTP_400_BAD_REQUEST
            )


"""
Views for users app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.user_service import UserService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError, ConflictError
from common.utils import get_client_ip
from apps.custom_auth.authentication import FirebaseAuthentication
from .serializers import (
    UserSerializer, UserPublicSerializer, UpdateUserProfileSerializer,
    UpdateUserSettingsSerializer, UserSearchSerializer, UserBulkSerializer,
    CreateUserSerializer
)


class CurrentUserView(APIView):
    """Get current user profile. Returns null if user doesn't exist in database yet."""
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = []  # No permission required, just authentication
    
    @swagger_auto_schema(
        operation_description="Get current user's full profile. Returns null if user not found in database.",
        responses={
            200: UserSerializer,
            204: "User authenticated but not found in database (returns null)"
        }
    )
    @rate_limit_general
    def get(self, request):
        """Get current user profile or null if not exists."""
        # If authentication succeeded, user exists
        if request.user and hasattr(request.user, 'user_id'):
            profile = UserService.get_current_user_profile(str(request.user.user_id))
            return Response(profile, status=status.HTTP_200_OK)
        
        # Firebase authenticated but user not in database
        if hasattr(request, 'firebase_uid'):
            return Response(data=None, status=status.HTTP_200_OK)
        
        # No authentication
        return Response(
            {'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required'}},
            status=status.HTTP_401_UNAUTHORIZED
        )


class CreateUserView(APIView):
    """Create a new user from Firebase authentication."""
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = []  # No permission required, just Firebase authentication
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Support file upload
    
    @swagger_auto_schema(
        operation_description="Create a new user account after Firebase authentication. Supports multipart/form-data for profile picture upload.",
        request_body=CreateUserSerializer,
        responses={
            201: UserSerializer,
            400: "Validation error",
            401: "Not authenticated with Firebase",
            409: "User already exists"
        }
    )
    @rate_limit_general
    def post(self, request):
        """Create new user from Firebase auth.
        
        Expected from JWT: firebase_uid, email
        Expected from request body: username (required), profile_picture (blob), bio, location, privacy (boolean)
        """
        # Check Firebase authentication. Allow tests that use `force_authenticate`
        # with a `User` instance (which doesn't set `request.firebase_uid`) by
        # falling back to `request.user.firebase_uid` if present.
        if not hasattr(request, 'firebase_uid'):
            if request.user and getattr(request.user, 'firebase_uid', None):
                request.firebase_uid = request.user.firebase_uid
                request.firebase_email = getattr(request.user, 'email', None)
            else:
                return Response(
                    {'error': {'code': 'UNAUTHORIZED', 'message': 'Firebase authentication required'}},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        # Check directly in PostgreSQL if user already exists by firebase_uid
        # This is more reliable than checking request.user state
        from db.entities.user_entity import User
        if User.objects.filter(firebase_uid=request.firebase_uid).exists():
            return Response(
                {'error': {'code': 'CONFLICT', 'message': 'User already registered'}},
                status=status.HTTP_409_CONFLICT
            )

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = UserService.create_user_from_firebase(
                firebase_uid=request.firebase_uid,
                email=request.firebase_email,
                **serializer.validated_data
            )
            profile = UserService.get_current_user_profile(str(user.user_id))
            return Response(profile, status=status.HTTP_201_CREATED)
        except ConflictError as e:
            return Response(
                {'error': {'code': 'CONFLICT', 'message': str(e)}},
                status=status.HTTP_409_CONFLICT
            )
        except ValidationError as e:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateCurrentUserView(APIView):
    """Update current user profile."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Update current user's profile",
        request_body=UpdateUserProfileSerializer,
        responses={200: UserSerializer}
    )
    @rate_limit_general
    def patch(self, request):
        """Update current user profile."""
        serializer = UpdateUserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = UserService.update_user_profile(
                str(request.user.user_id),
                **serializer.validated_data
            )
            profile = UserService.get_current_user_profile(str(user.user_id))
            return Response(profile, status=status.HTTP_200_OK)
        except ConflictError as e:
            return Response(
                {'error': {'code': 'CONFLICT', 'message': str(e)}},
                status=status.HTTP_409_CONFLICT
            )


class UpdateCurrentUserSettingsView(APIView):
    """Update current user settings."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Update current user's settings",
        request_body=UpdateUserSettingsSerializer,
        responses={200: UpdateUserSettingsSerializer}
    )
    @rate_limit_general
    def patch(self, request):
        """Update current user settings."""
        serializer = UpdateUserSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        settings = UserService.update_user_settings(
            str(request.user.user_id),
            **serializer.validated_data
        )
        
        return Response({
            'email_notifications': settings.email_notifications,
            'language': settings.language
        }, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """Get user public profile."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get user's public profile",
        responses={200: UserPublicSerializer}
    )
    @rate_limit_general
    def get(self, request, user_id):
        """Get user public profile."""
        try:
            # Check if viewer can view profile
            if not UserService.can_view_profile(str(request.user.user_id), user_id):
                return Response(
                    {'error': {'code': 'FORBIDDEN', 'message': 'Cannot view private profile'}},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user = UserService.get_user_by_id(user_id)
            return Response({
                'user_id': str(user.user_id),
                'username': user.username,
                'display_name': user.profile.display_name,
                'profile_picture_url': user.profile.profile_picture_url,
                'bio': user.profile.bio,
                'location': user.profile.location,
                'created_at': user.created_at
            }, status=status.HTTP_200_OK)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class BlockUserView(APIView):
    """Block a user."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Block a user",
        responses={204: 'User blocked successfully'}
    )
    @rate_limit_general
    def post(self, request, user_id):
        """Block a user."""
        try:
            ip_address = get_client_ip(request)
            UserService.block_user(str(request.user.user_id), user_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (ValidationError, ConflictError) as e:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class UnblockUserView(APIView):
    """Unblock a user."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Unblock a user",
        responses={204: 'User unblocked successfully'}
    )
    @rate_limit_general
    def delete(self, request, user_id):
        """Unblock a user."""
        try:
            ip_address = get_client_ip(request)
            UserService.unblock_user(str(request.user.user_id), user_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class BlockedUsersView(APIView):
    """Get list of blocked users."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get list of blocked users",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: UserPublicSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get blocked users."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        users = UserService.get_blocked_users(str(request.user.user_id), page, page_size)

        data = [{
            'user_id': str(user.user_id),
            'username': user.username,
            'display_name': user.profile.display_name,
            'profile_picture_url': user.profile.profile_picture_url
        } for user in users]

        return Response(data, status=status.HTTP_200_OK)


class UserSearchView(APIView):
    """Search users."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Search users by username",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: UserPublicSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Search users."""
        query = request.query_params.get('query', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        if not query:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': 'Query parameter is required'}},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = UserService.search_users(query, str(request.user.user_id), page, page_size)

        data = [{
            'user_id': str(user.user_id),
            'username': user.username,
            'display_name': user.profile.display_name,
            'profile_picture_url': user.profile.profile_picture_url
        } for user in users]

        return Response(data, status=status.HTTP_200_OK)


class UserBulkView(APIView):
    """Get multiple users by IDs."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get multiple users by IDs",
        request_body=UserBulkSerializer,
        responses={200: UserPublicSerializer(many=True)}
    )
    @rate_limit_general
    def post(self, request):
        """Get bulk users."""
        serializer = UserBulkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_ids = [str(uid) for uid in serializer.validated_data['user_ids']]
        users = UserService.get_bulk_users(user_ids)

        data = [{
            'user_id': str(user.user_id),
            'username': user.username,
            'display_name': user.profile.display_name,
            'profile_picture_url': user.profile.profile_picture_url
        } for user in users]

        return Response(data, status=status.HTTP_200_OK)


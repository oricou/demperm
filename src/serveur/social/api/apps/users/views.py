"""
Views for users app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.user_service import UserService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError, ConflictError
from common.utils import get_client_ip
from .serializers import (
    UserSerializer, UserPublicSerializer, UpdateUserProfileSerializer,
    UpdateUserSettingsSerializer, UserSearchSerializer, UserBulkSerializer
)


class CurrentUserView(APIView):
    """Get current user profile."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get current user's full profile",
        responses={200: UserSerializer}
    )
    @rate_limit_general
    def get(self, request):
        """Get current user profile."""
        profile = UserService.get_current_user_profile(str(request.user.user_id))
        return Response(profile, status=status.HTTP_200_OK)


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


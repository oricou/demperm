"""
Views for followers app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.follower_service import FollowerService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError, ConflictError
from common.utils import get_client_ip
from .serializers import FollowSerializer, UserFollowSerializer


class FollowUserView(APIView):
    """Follow a user."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Follow a user (auto-accepted for public, pending for private)",
        responses={201: FollowSerializer}
    )
    @rate_limit_general
    def post(self, request, user_id):
        """Follow user."""
        try:
            ip_address = get_client_ip(request)
            follow = FollowerService.follow_user(str(request.user.user_id), user_id, ip_address)
            
            return Response({
                'follow_id': str(follow.follow_id),
                'follower_id': str(follow.follower_id),
                'followed_id': str(follow.followed_id),
                'status': follow.status,
                'created_at': follow.created_at
            }, status=status.HTTP_201_CREATED)
        except (ValidationError, ConflictError) as e:
            return Response(
                {'error': {'code': 'ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class UnfollowUserView(APIView):
    """Unfollow a user."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Unfollow a user",
        responses={204: 'Unfollowed successfully'}
    )
    @rate_limit_general
    def delete(self, request, user_id):
        """Unfollow user."""
        try:
            ip_address = get_client_ip(request)
            FollowerService.unfollow_user(str(request.user.user_id), user_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class AcceptFollowRequestView(APIView):
    """Accept a follow request."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Accept a follow request",
        responses={200: FollowSerializer}
    )
    @rate_limit_general
    def post(self, request, user_id):
        """Accept follow request."""
        try:
            ip_address = get_client_ip(request)
            follow = FollowerService.accept_follow_request(str(request.user.user_id), user_id, ip_address)
            
            return Response({
                'follow_id': str(follow.follow_id),
                'follower_id': str(follow.follower_id),
                'followed_id': str(follow.followed_id),
                'status': follow.status,
                'created_at': follow.created_at
            }, status=status.HTTP_200_OK)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class RejectFollowRequestView(APIView):
    """Reject a follow request."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Reject a follow request",
        responses={204: 'Rejected successfully'}
    )
    @rate_limit_general
    def post(self, request, user_id):
        """Reject follow request."""
        try:
            ip_address = get_client_ip(request)
            FollowerService.reject_follow_request(str(request.user.user_id), user_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class FollowersListView(APIView):
    """Get user's followers."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get user's followers",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: UserFollowSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get followers."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        followers = FollowerService.get_followers(str(request.user.user_id), page, page_size)
        
        data = [{
            'user_id': str(user.user_id),
            'username': user.username,
            'display_name': user.profile.display_name,
            'profile_picture_url': user.profile.profile_picture_url
        } for user in followers]
        
        return Response(data, status=status.HTTP_200_OK)


class FollowingListView(APIView):
    """Get users that current user follows."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get users that current user follows",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: UserFollowSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get following."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        following = FollowerService.get_following(str(request.user.user_id), page, page_size)
        
        data = [{
            'user_id': str(user.user_id),
            'username': user.username,
            'display_name': user.profile.display_name,
            'profile_picture_url': user.profile.profile_picture_url
        } for user in following]
        
        return Response(data, status=status.HTTP_200_OK)


class PendingRequestsView(APIView):
    """Get pending follow requests."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get pending follow requests",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: FollowSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get pending requests."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        requests = FollowerService.get_pending_requests(str(request.user.user_id), page, page_size)

        data = [{
            'follow_id': str(req.follow_id),
            'follower_id': str(req.follower_id),
            'followed_id': str(req.followed_id),
            'status': req.status,
            'created_at': req.created_at
        } for req in requests]

        return Response(data, status=status.HTTP_200_OK)


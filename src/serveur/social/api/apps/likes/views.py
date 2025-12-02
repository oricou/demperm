"""
Views for likes app (proxied endpoints to PostService).
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.post_service import PostService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ConflictError
from common.utils import get_client_ip
from apps.posts.serializers import LikeSerializer


class LikePostView(APIView):
    """Like a post (proxy)."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Like a post",
        responses={201: LikeSerializer}
    )
    @rate_limit_general
    def post(self, request, post_id):
        try:
            ip_address = get_client_ip(request)
            like = PostService.like_post(post_id, str(request.user.user_id), ip_address)

            return Response({
                'like_id': str(like.like_id),
                'user_id': str(like.user_id),
                'post_id': str(like.post_id),
                'created_at': like.created_at
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': {'code': 'ERROR', 'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(APIView):
    """Unlike a post (proxy)."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Unlike a post",
        responses={204: 'Post unliked successfully'}
    )
    @rate_limit_general
    def delete(self, request, post_id):
        try:
            ip_address = get_client_ip(request)
            PostService.unlike_post(post_id, str(request.user.user_id), ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response({'error': {'code': 'NOT_FOUND', 'message': str(e)}}, status=status.HTTP_404_NOT_FOUND)


class PostLikesView(APIView):
    """Get post likes (proxy)."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get users who liked the post",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: LikeSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request, post_id):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        likes = PostService.get_post_likes(post_id, page, page_size)

        data = [{
            'like_id': str(like.like_id),
            'user_id': str(like.user_id),
            'username': like.user.username,
            'post_id': str(like.post_id),
            'created_at': like.created_at
        } for like in likes]

        return Response(data, status=status.HTTP_200_OK)

"""
Views for posts app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.post_service import PostService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_post_create, rate_limit_general
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError
from common.utils import get_client_ip
from .serializers import CreatePostSerializer, PostSerializer, LikeSerializer


class CreatePostView(APIView):
    """Create a new post."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=CreatePostSerializer,
        responses={201: PostSerializer}
    )
    @rate_limit_post_create
    def post(self, request):
        """Create a post."""
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            ip_address = get_client_ip(request)
            post = PostService.create_post(
                user_id=str(request.user.user_id),
                title=serializer.validated_data['title'],
                content=serializer.validated_data['content'],
                subforum_id=str(serializer.validated_data['subforum_id']),
                ip_address=ip_address
            )
            
            return Response({
                'post_id': str(post.post_id),
                'author_id': str(post.author_id),
                'subforum_id': str(post.subforum_id),
                'title': post.title,
                'content': post.content,
                'content_signature': post.content_signature,
                'like_count': post.like_count,
                'comment_count': post.comment_count,
                'created_at': post.created_at,
                'updated_at': post.updated_at
            }, status=status.HTTP_201_CREATED)
        except (ValidationError, NotFoundError) as e:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class PostDetailView(APIView):
    """Get post details."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get post details",
        responses={200: PostSerializer}
    )
    @rate_limit_general
    def get(self, request, post_id):
        """Get post."""
        try:
            post = PostService.get_post_by_id(post_id, str(request.user.user_id))
            
            return Response({
                'post_id': str(post.post_id),
                'author_id': str(post.author_id),
                'author_username': post.author.username,
                'subforum_id': str(post.subforum_id),
                'title': post.title,
                'content': post.content,
                'content_signature': post.content_signature,
                'like_count': post.like_count,
                'comment_count': post.comment_count,
                'created_at': post.created_at,
                'updated_at': post.updated_at
            }, status=status.HTTP_200_OK)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDeniedError as e:
            return Response(
                {'error': {'code': 'FORBIDDEN', 'message': str(e)}},
                status=status.HTTP_403_FORBIDDEN
            )


class DeletePostView(APIView):
    """Delete a post."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Delete a post",
        responses={204: 'Post deleted successfully'}
    )
    @rate_limit_general
    def delete(self, request, post_id):
        """Delete post."""
        try:
            ip_address = get_client_ip(request)
            PostService.delete_post(post_id, str(request.user.user_id), ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDeniedError as e:
            return Response(
                {'error': {'code': 'FORBIDDEN', 'message': str(e)}},
                status=status.HTTP_403_FORBIDDEN
            )


class LikePostView(APIView):
    """Like a post."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Like a post",
        responses={201: LikeSerializer}
    )
    @rate_limit_general
    def post(self, request, post_id):
        """Like post."""
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
            return Response(
                {'error': {'code': 'ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class UnlikePostView(APIView):
    """Unlike a post."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Unlike a post",
        responses={204: 'Post unliked successfully'}
    )
    @rate_limit_general
    def delete(self, request, post_id):
        """Unlike post."""
        try:
            ip_address = get_client_ip(request)
            PostService.unlike_post(post_id, str(request.user.user_id), ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class PostLikesView(APIView):
    """Get post likes."""

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
        """Get post likes."""
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


class FeedView(APIView):
    """Get personalized feed."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get personalized feed from followed users",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: PostSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get feed."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        posts = PostService.get_feed(str(request.user.user_id), page, page_size)

        data = [{
            'post_id': str(post.post_id),
            'author_id': str(post.author_id),
            'author_username': post.author.username,
            'subforum_id': str(post.subforum_id),
            'title': post.title,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'like_count': post.like_count,
            'comment_count': post.comment_count,
            'created_at': post.created_at
        } for post in posts]

        return Response(data, status=status.HTTP_200_OK)


class DiscoverView(APIView):
    """Get discover feed."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get discover feed with trending posts",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: PostSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get discover feed."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        posts = PostService.get_discover(str(request.user.user_id), page, page_size)

        data = [{
            'post_id': str(post.post_id),
            'author_id': str(post.author_id),
            'author_username': post.author.username,
            'subforum_id': str(post.subforum_id),
            'title': post.title,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'like_count': post.like_count,
            'comment_count': post.comment_count,
            'created_at': post.created_at
        } for post in posts]

        return Response(data, status=status.HTTP_200_OK)


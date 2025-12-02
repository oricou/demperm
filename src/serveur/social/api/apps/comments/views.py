"""
Views for comments app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.comment_service import CommentService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_comment_create, rate_limit_general
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError
from common.utils import get_client_ip
from .serializers import CreateCommentSerializer, CommentSerializer


class PostCommentsView(APIView):
    """Get comments for a post."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get comments for a post",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20),
            openapi.Parameter('sort_by', openapi.IN_QUERY, type=openapi.TYPE_STRING, default='created_at')
        ],
        responses={200: CommentSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request, post_id):
        """Get post comments."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        sort_by = request.query_params.get('sort_by', 'created_at')
        
        comments = CommentService.get_post_comments(post_id, page, page_size, sort_by)
        
        data = [{
            'comment_id': str(comment.comment_id),
            'post_id': str(comment.post_id),
            'author_id': str(comment.author_id),
            'author_username': comment.author.username,
            'parent_comment_id': str(comment.parent_comment_id) if comment.parent_comment_id else None,
            'content': comment.content,
            'created_at': comment.created_at,
            'updated_at': comment.updated_at
        } for comment in comments]
        
        return Response(data, status=status.HTTP_200_OK)


class CreateCommentView(APIView):
    """Create a comment on a post."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Create a comment on a post",
        request_body=CreateCommentSerializer,
        responses={201: CommentSerializer}
    )
    @rate_limit_comment_create
    def post(self, request, post_id):
        """Create comment."""
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            ip_address = get_client_ip(request)
            comment = CommentService.create_comment(
                user_id=str(request.user.user_id),
                post_id=post_id,
                content=serializer.validated_data['content'],
                parent_comment_id=str(serializer.validated_data.get('parent_comment_id')) if serializer.validated_data.get('parent_comment_id') else None,
                ip_address=ip_address
            )
            
            return Response({
                'comment_id': str(comment.comment_id),
                'post_id': str(comment.post_id),
                'author_id': str(comment.author_id),
                'parent_comment_id': str(comment.parent_comment_id) if comment.parent_comment_id else None,
                'content': comment.content,
                'created_at': comment.created_at,
                'updated_at': comment.updated_at
            }, status=status.HTTP_201_CREATED)
        except (ValidationError, NotFoundError) as e:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class DeleteCommentView(APIView):
    """Delete a comment."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Delete a comment",
        responses={204: 'Comment deleted successfully'}
    )
    @rate_limit_general
    def delete(self, request, comment_id):
        """Delete comment."""
        try:
            ip_address = get_client_ip(request)
            CommentService.delete_comment(comment_id, str(request.user.user_id), ip_address)
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


class CommentRepliesView(APIView):
    """Get replies to a comment."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get replies to a comment",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: CommentSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request, comment_id):
        """Get comment replies."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        replies = CommentService.get_comment_replies(comment_id, page, page_size)
        
        data = [{
            'comment_id': str(reply.comment_id),
            'post_id': str(reply.post_id),
            'author_id': str(reply.author_id),
            'author_username': reply.author.username,
            'parent_comment_id': str(reply.parent_comment_id),
            'content': reply.content,
            'created_at': reply.created_at,
            'updated_at': reply.updated_at
        } for reply in replies]
        
        return Response(data, status=status.HTTP_200_OK)


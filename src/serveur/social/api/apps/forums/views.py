"""
Views for forums app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.forum_service import ForumService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError, ConflictError
from common.utils import get_client_ip
from .serializers import ForumSerializer, CreateForumSerializer


class ForumsListView(APIView):
    """Get all forums."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get all forums",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: ForumSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get all forums."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        forums = ForumService.get_all_forums(page, page_size)
        
        data = [{
            'forum_id': str(forum.forum_id),
            'name': forum.name,
            'description': forum.description,
            'creator_id': str(forum.creator_id),
            'member_count': forum.member_count,
            'post_count': forum.post_count,
            'created_at': forum.created_at
        } for forum in forums]
        
        return Response(data, status=status.HTTP_200_OK)


class CreateForumView(APIView):
    """Create a new forum."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Create a new forum",
        request_body=CreateForumSerializer,
        responses={201: ForumSerializer}
    )
    @rate_limit_general
    def post(self, request):
        """Create forum."""
        serializer = CreateForumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            ip_address = get_client_ip(request)
            forum = ForumService.create_forum(
                user_id=str(request.user.user_id),
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                ip_address=ip_address
            )
            
            return Response({
                'forum_id': str(forum.forum_id),
                'name': forum.name,
                'description': forum.description,
                'creator_id': str(forum.creator_id),
                'member_count': forum.member_count,
                'post_count': forum.post_count,
                'created_at': forum.created_at
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class ForumDetailView(APIView):
    """Get forum details."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get forum details",
        responses={200: ForumSerializer}
    )
    @rate_limit_general
    def get(self, request, forum_id):
        """Get forum."""
        try:
            forum = ForumService.get_forum_by_id(forum_id)
            
            return Response({
                'forum_id': str(forum.forum_id),
                'name': forum.name,
                'description': forum.description,
                'creator_id': str(forum.creator_id),
                'member_count': forum.member_count,
                'post_count': forum.post_count,
                'created_at': forum.created_at
            }, status=status.HTTP_200_OK)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class SearchForumsView(APIView):
    """Search forums."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Search forums by name",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: ForumSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Search forums."""
        query = request.query_params.get('query', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        if not query:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': 'Query parameter is required'}},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        forums = ForumService.search_forums(query, page, page_size)
        
        data = [{
            'forum_id': str(forum.forum_id),
            'name': forum.name,
            'description': forum.description,
            'member_count': forum.member_count,
            'post_count': forum.post_count
        } for forum in forums]
        
        return Response(data, status=status.HTTP_200_OK)


class JoinForumView(APIView):
    """Join a forum."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Join a forum",
        responses={201: 'Joined forum successfully'}
    )
    @rate_limit_general
    def post(self, request, forum_id):
        """Join forum."""
        try:
            ip_address = get_client_ip(request)
            ForumService.join_forum(str(request.user.user_id), forum_id, ip_address)
            return Response({'message': 'Joined forum successfully'}, status=status.HTTP_201_CREATED)
        except (NotFoundError, ConflictError) as e:
            return Response(
                {'error': {'code': 'ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class LeaveForumView(APIView):
    """Leave a forum."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Leave a forum",
        responses={204: 'Left forum successfully'}
    )
    @rate_limit_general
    def delete(self, request, forum_id):
        """Leave forum."""
        try:
            ip_address = get_client_ip(request)
            ForumService.leave_forum(str(request.user.user_id), forum_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


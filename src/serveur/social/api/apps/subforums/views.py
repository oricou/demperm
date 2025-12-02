"""
Views for subforums app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.domain_service import DomainService
from db.repositories.post_repository import PostRepository
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError

from .serializers import SubforumSerializer, PostSummarySerializer


class SubforumDetailView(APIView):
    """Get subforum details."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get subforum details",
        responses={200: SubforumSerializer}
    )
    @rate_limit_general
    def get(self, request, subforum_id):
        """Return subforum details."""
        try:
            subforum = DomainService.get_subforum_by_id(subforum_id)

            return Response({
                'subforum_id': str(subforum.subforum_id),
                'name': subforum.name,
                'description': subforum.description,
                'parent_domain_id': str(subforum.parent_domain_id) if subforum.parent_domain_id else None,
                'parent_forum_id': str(subforum.parent_forum_id) if subforum.parent_forum_id else None,
                'post_count': subforum.post_count,
                'created_at': subforum.created_at
            }, status=status.HTTP_200_OK)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class SubforumPostsView(APIView):
    """List posts in a subforum."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="List posts in a subforum",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: PostSummarySerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request, subforum_id):
        """Return posts in subforum."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        try:
            # Ensure subforum exists
            DomainService.get_subforum_by_id(subforum_id)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )

        posts = PostRepository.get_by_subforum(subforum_id, page, page_size)

        data = [{
            'post_id': str(post.post_id),
            'user_id': str(post.user_id),
            'title': post.title,
            'like_count': post.like_count,
            'comment_count': post.comment_count,
            'created_at': post.created_at
        } for post in posts]

        return Response(data, status=status.HTTP_200_OK)

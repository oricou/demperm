"""
Views for tags app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.tag_service import TagService
from common.permissions import IsAuthenticated, IsNotBanned, IsAdmin
from common.rate_limiters import rate_limit_general
from common.exceptions import ValidationError, NotFoundError, ConflictError
from common.utils import get_client_ip
from .serializers import TagSerializer, CreateTagSerializer, AssignTagsSerializer


class TagsListView(APIView):
    """List tags."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="List tags",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=100)
        ],
        responses={200: TagSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 100))

        tags = TagService.get_all_tags(page, page_size)

        data = [{
            'tag_id': str(tag.tag_id),
            'tag_name': tag.tag_name,
            'creator_id': str(tag.creator_id) if tag.creator_id else None,
            'created_at': tag.created_at
        } for tag in tags]

        return Response(data, status=status.HTTP_200_OK)


class CreateTagView(APIView):
    """Create a tag."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Create a new tag",
        request_body=CreateTagSerializer,
        responses={201: TagSerializer}
    )
    @rate_limit_general
    def post(self, request):
        serializer = CreateTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tag = TagService.create_tag(str(request.user.user_id), serializer.validated_data['tag_name'])
            return Response({
                'tag_id': str(tag.tag_id),
                'tag_name': tag.tag_name,
                'creator_id': str(tag.creator_id) if tag.creator_id else None,
                'created_at': tag.created_at
            }, status=status.HTTP_201_CREATED)
        except ConflictError as e:
            return Response({'error': {'code': 'CONFLICT', 'message': str(e)}}, status=status.HTTP_409_CONFLICT)
        except ValidationError as e:
            return Response({'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)


class DeleteTagView(APIView):
    """Delete a tag (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(operation_description="Delete a tag", responses={204: 'Deleted'})
    @rate_limit_general
    def delete(self, request, tag_id):
        try:
            # Admin-only deletion; repository handles cascade
            from db.repositories.tag_repository import TagRepository
            if not TagRepository.get_by_id(tag_id):
                raise NotFoundError("Tag not found")
            TagRepository.delete(tag_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response({'error': {'code': 'NOT_FOUND', 'message': str(e)}}, status=status.HTTP_404_NOT_FOUND)


class AssignTagsView(APIView):
    """Assign tags to a post."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Assign tags to a post",
        request_body=AssignTagsSerializer,
        responses={200: 'Tags assigned'}
    )
    @rate_limit_general
    def post(self, request, post_id):
        serializer = AssignTagsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            TagService.assign_tags_to_post(str(request.user.user_id), post_id, [str(t) for t in serializer.validated_data['tags']])
            return Response({'message': 'Tags assigned'}, status=status.HTTP_200_OK)
        except (ValidationError, NotFoundError, ConflictError) as e:
            return Response({'error': {'code': 'ERROR', 'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)


class UnassignTagsView(APIView):
    """Unassign tags from a post."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Unassign tags from a post",
        request_body=AssignTagsSerializer,
        responses={200: 'Tags unassigned'}
    )
    @rate_limit_general
    def post(self, request, post_id):
        serializer = AssignTagsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            TagService.unassign_tags_from_post(str(request.user.user_id), post_id, [str(t) for t in serializer.validated_data['tags']])
            return Response({'message': 'Tags unassigned'}, status=status.HTTP_200_OK)
        except (ValidationError, NotFoundError) as e:
            return Response({'error': {'code': 'ERROR', 'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)

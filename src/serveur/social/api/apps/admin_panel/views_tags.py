"""
Admin panel views for tag management.
"""
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.permissions import IsAuthenticated, IsAdmin
from common.rate_limiters import rate_limit_general
from db.repositories.tag_repository import TagRepository
from db.repositories.message_repository import AuditLogRepository
from common.utils import get_client_ip
from .response_utils import api_success, api_error


class DeleteTagView(APIView):
    """Delete a tag (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Delete a tag by tag_id (query param)",
        manual_parameters=[
            openapi.Parameter('tag_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ],
        responses={204: 'Tag deleted'}
    )
    @rate_limit_general
    def delete(self, request):
        tag_id = request.query_params.get('tag_id')
        if not tag_id:
            return api_error('VALIDATION_ERROR', 'tag_id is required', status_code=400)
        deleted = TagRepository.delete(tag_id)
        if not deleted:
            return api_error('NOT_FOUND', 'Tag not found', status_code=404)
        AuditLogRepository.create(
            user_id=str(request.user.user_id),
            action_type='delete',
            resource_type='tag',
            resource_id=tag_id,
            ip_address=get_client_ip(request)
        )
        return api_success(status_code=204)

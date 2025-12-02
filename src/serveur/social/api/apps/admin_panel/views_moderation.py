"""
Admin panel views for moderation (ban/unban, remove content).
"""
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from common.permissions import IsAuthenticated, IsAdmin
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, PermissionDeniedError, ValidationError
from common.utils import get_client_ip
from services.apps_services.report_service import ReportService
from db.repositories.post_repository import PostRepository, CommentRepository
from db.repositories.message_repository import AuditLogRepository
from .response_utils import api_success, api_error


def _invalidate_tokens(user_id: str):
    """Best-effort refresh token invalidation."""
    try:
        from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
        tokens = OutstandingToken.objects.filter(user_id=user_id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
    except Exception:
        # If blacklist app is not available, silently ignore (best-effort)
        return


class BanUserView(APIView):
    """Ban a user (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Ban a user",
        responses={204: 'User banned successfully'}
    )
    @rate_limit_general
    def post(self, request, user_id):
        try:
            ip_address = get_client_ip(request)
            ReportService.ban_user(str(request.user.user_id), user_id, ip_address)
            _invalidate_tokens(user_id)
            return api_success(status_code=204)
        except (NotFoundError, PermissionDeniedError, ValidationError) as e:
            return api_error('ERROR', str(e), status_code=400)


class UnbanUserView(APIView):
    """Unban a user (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Unban a user",
        responses={204: 'User unbanned successfully'}
    )
    @rate_limit_general
    def post(self, request, user_id):
        try:
            ip_address = get_client_ip(request)
            ReportService.unban_user(str(request.user.user_id), user_id, ip_address)
            return api_success(status_code=204)
        except NotFoundError as e:
            return api_error('NOT_FOUND', str(e), status_code=404)


class RemovePostView(APIView):
    """Remove a post (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Remove a post",
        responses={204: 'Post removed'}
    )
    @rate_limit_general
    def delete(self, request, post_id):
        post = PostRepository.get_by_id(post_id)
        if not post:
            return api_error('NOT_FOUND', 'Post not found', status_code=404)
        PostRepository.delete(post_id)
        AuditLogRepository.create(
            user_id=str(request.user.user_id),
            action_type='delete',
            resource_type='post',
            resource_id=post_id,
            ip_address=get_client_ip(request)
        )
        return api_success(status_code=204)


class RemoveCommentView(APIView):
    """Remove a comment (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Remove a comment",
        responses={204: 'Comment removed'}
    )
    @rate_limit_general
    def delete(self, request, comment_id):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            return api_error('NOT_FOUND', 'Comment not found', status_code=404)
        CommentRepository.delete(comment_id)
        AuditLogRepository.create(
            user_id=str(request.user.user_id),
            action_type='delete',
            resource_type='comment',
            resource_id=comment_id,
            ip_address=get_client_ip(request)
        )
        return api_success(status_code=204)

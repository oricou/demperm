"""
Admin panel views for reports moderation.
"""
from typing import Optional, Dict
from django.utils import timezone
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.permissions import IsAuthenticated, IsAdmin
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError
from common.utils import get_client_ip
from services.apps_services.report_service import ReportService
from db.repositories.post_repository import PostRepository, CommentRepository
from db.repositories.user_repository import UserRepository
from db.entities.message_entity import Report as ReportModel
from .serializers import UpdateReportStatusSerializer, ReportSerializer, ReportActionSerializer
from .response_utils import api_success, api_error


def _build_target_preview(report: ReportModel) -> Optional[Dict]:
    """Construct a lightweight preview of the reported target."""
    if report.target_type == 'post':
        post = PostRepository.get_by_id(str(report.target_id))
        if not post:
            return None
        content = (post.content or "")[:120]
        return {'title': post.title, 'content': content}
    if report.target_type == 'comment':
        comment = CommentRepository.get_by_id(str(report.target_id))
        if not comment:
            return None
        return {'content': (comment.content or "")[:120]}
    if report.target_type == 'user':
        user = UserRepository.get_by_id(str(report.target_id))
        if not user:
            return None
        return {'username': user.username, 'user_id': str(user.user_id)}
    return None


def _serialize_report(report: ReportModel) -> Dict:
    """Serialize report with reporter info and target preview."""
    reporter = report.reporter
    return {
        'report_id': str(report.report_id),
        'reporter': {
            'user_id': str(reporter.user_id) if reporter else None,
            'username': reporter.username if reporter else None,
        },
        'target_type': report.target_type,
        'target_id': str(report.target_id),
        'target_preview': _build_target_preview(report),
        'reason': report.reason,
        'description': report.description,
        'status': report.status,
        'resolved_by': str(report.resolved_by_id) if report.resolved_by_id else None,
        'created_at': report.created_at,
        'resolved_at': report.resolved_at,
    }


class ReportsListView(APIView):
    """Get all reports (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Get all reports",
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: ReportSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        status_filter = request.query_params.get('status', None)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        allowed_status = {'pending', 'resolved', 'rejected'}
        if status_filter and status_filter not in allowed_status:
            return api_error('VALIDATION_ERROR', 'Invalid status filter', status_code=400)

        reports, total = ReportService.get_all_reports(status_filter, page, page_size)

        payload = {'reports': [_serialize_report(r) for r in reports]}
        total_pages = (total + page_size - 1) // page_size if page_size else 1
        pagination = {
            'page': page,
            'page_size': page_size,
            'total_items': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_previous': page > 1
        }
        return api_success(data=payload, pagination=pagination, status_code=200)


class ResolveReportView(APIView):
    """Resolve a report (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Resolve a report",
        request_body=ReportActionSerializer,
        responses={200: ReportSerializer}
    )
    @rate_limit_general
    def post(self, request, report_id):
        serializer = ReportActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ip_address = get_client_ip(request)
            report = ReportService.update_report_status(
                report_id=report_id,
                admin_id=str(request.user.user_id),
                status='resolved',
                ip_address=ip_address,
                action_details=serializer.validated_data,
            )
            return api_success(data=_serialize_report(report), status_code=200)
        except NotFoundError as e:
            return api_error('NOT_FOUND', str(e), status_code=404)
        except (ValidationError, PermissionDeniedError) as e:
            return api_error('VALIDATION_ERROR', str(e), status_code=400)


class RejectReportView(APIView):
    """Reject a report (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Reject a report",
        request_body=ReportActionSerializer,
        responses={200: ReportSerializer}
    )
    @rate_limit_general
    def post(self, request, report_id):
        serializer = ReportActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ip_address = get_client_ip(request)
            report = ReportService.update_report_status(
                report_id=report_id,
                admin_id=str(request.user.user_id),
                status='rejected',
                ip_address=ip_address,
                action_details=serializer.validated_data,
            )
            return api_success(data=_serialize_report(report), status_code=200)
        except NotFoundError as e:
            return api_error('NOT_FOUND', str(e), status_code=404)
        except (ValidationError, PermissionDeniedError) as e:
            return api_error('VALIDATION_ERROR', str(e), status_code=400)

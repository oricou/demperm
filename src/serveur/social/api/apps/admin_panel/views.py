"""
Views for admin_panel app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.report_service import ReportService
from common.permissions import IsAuthenticated, IsAdmin
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, PermissionDeniedError
from common.utils import get_client_ip
from .serializers import UpdateReportStatusSerializer, ReportSerializer


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
        """Get reports."""
        status_filter = request.query_params.get('status', None)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        reports = ReportService.get_all_reports(status_filter, page, page_size)
        
        data = [{
            'report_id': str(report.report_id),
            'reporter_id': str(report.reporter_id),
            'target_type': report.target_type,
            'target_id': str(report.target_id),
            'reason': report.reason,
            'status': report.status,
            'created_at': report.created_at,
            'resolved_at': report.resolved_at
        } for report in reports]
        
        return Response(data, status=status.HTTP_200_OK)


class UpdateReportStatusView(APIView):
    """Update report status (admin only)."""
    
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Update report status",
        request_body=UpdateReportStatusSerializer,
        responses={200: ReportSerializer}
    )
    @rate_limit_general
    def post(self, request, report_id):
        """Update report status."""
        serializer = UpdateReportStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            ip_address = get_client_ip(request)
            report = ReportService.update_report_status(
                report_id=report_id,
                admin_id=str(request.user.user_id),
                status=serializer.validated_data['status'],
                ip_address=ip_address
            )
            
            return Response({
                'report_id': str(report.report_id),
                'status': report.status,
                'resolved_at': report.resolved_at
            }, status=status.HTTP_200_OK)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class BanUserView(APIView):
    """Ban a user (admin only)."""
    
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Ban a user",
        responses={204: 'User banned successfully'}
    )
    @rate_limit_general
    def post(self, request, user_id):
        """Ban user."""
        try:
            ip_address = get_client_ip(request)
            ReportService.ban_user(str(request.user.user_id), user_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (NotFoundError, PermissionDeniedError) as e:
            return Response(
                {'error': {'code': 'ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class UnbanUserView(APIView):
    """Unban a user (admin only)."""
    
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Unban a user",
        responses={204: 'User unbanned successfully'}
    )
    @rate_limit_general
    def delete(self, request, user_id):
        """Unban user."""
        try:
            ip_address = get_client_ip(request)
            ReportService.unban_user(str(request.user.user_id), user_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


"""
Views for reports app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from services.apps_services.report_service import ReportService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError
from common.utils import get_client_ip
from .serializers import CreateReportSerializer, ReportSerializer


class CreateReportView(APIView):
    """Create a report."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Create a report for a post, comment, or user",
        request_body=CreateReportSerializer,
        responses={201: ReportSerializer}
    )
    @rate_limit_general
    def post(self, request):
        """Create report."""
        serializer = CreateReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            ip_address = get_client_ip(request)
            report = ReportService.create_report(
                reporter_id=str(request.user.user_id),
                target_type=serializer.validated_data['target_type'],
                target_id=str(serializer.validated_data['target_id']),
                reason=serializer.validated_data['reason'],
                ip_address=ip_address
            )
            
            return Response({
                'report_id': str(report.report_id),
                'reporter_id': str(report.reporter_id),
                'target_type': report.target_type,
                'target_id': str(report.target_id),
                'reason': report.reason,
                'status': report.status,
                'created_at': report.created_at
            }, status=status.HTTP_201_CREATED)
        except (ValidationError, NotFoundError) as e:
            return Response(
                {'error': {'code': 'ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


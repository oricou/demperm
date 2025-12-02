"""
Admin panel views for domains management.
"""
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from common.permissions import IsAuthenticated, IsAdmin
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError
from common.utils import get_client_ip
from services.apps_services.domain_service import DomainService
from .serializers import DomainCreateUpdateSerializer
from .response_utils import api_success, api_error


class AdminDomainCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Create a domain",
        request_body=DomainCreateUpdateSerializer,
        responses={201: 'Domain created'}
    )
    @rate_limit_general
    def post(self, request):
        serializer = DomainCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            domain = DomainService.create_domain(
                admin_id=str(request.user.user_id),
                domain_name=serializer.validated_data['domain_name'],
                description=serializer.validated_data.get('description'),
                icon_url=serializer.validated_data.get('icon_url'),
                ip_address=get_client_ip(request)
            )
            return api_success(
                data={
                    'domain_id': str(domain.domain_id),
                    'domain_name': domain.domain_name,
                    'description': domain.description,
                    'icon_url': domain.icon_url,
                    'created_at': domain.created_at,
                },
                status_code=201
            )
        except ValidationError as e:
            return api_error('VALIDATION_ERROR', str(e), status_code=400)


class AdminDomainUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Update or delete a domain",
        request_body=DomainCreateUpdateSerializer,
        responses={200: 'Domain updated'}
    )
    @rate_limit_general
    def patch(self, request, domain_id):
        serializer = DomainCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            domain = DomainService.update_domain(
                admin_id=str(request.user.user_id),
                domain_id=domain_id,
                domain_name=serializer.validated_data.get('domain_name'),
                description=serializer.validated_data.get('description'),
                icon_url=serializer.validated_data.get('icon_url'),
                ip_address=get_client_ip(request)
            )
            return api_success(
                data={
                    'domain_id': str(domain.domain_id),
                    'domain_name': domain.domain_name,
                    'description': domain.description,
                    'icon_url': domain.icon_url,
                    'updated_at': getattr(domain, 'updated_at', None),
                },
                status_code=200
            )
        except NotFoundError as e:
            return api_error('NOT_FOUND', str(e), status_code=404)
        except ValidationError as e:
            return api_error('VALIDATION_ERROR', str(e), status_code=400)

    @swagger_auto_schema(
        operation_description="Delete a domain",
        responses={204: 'Domain deleted'}
    )
    @rate_limit_general
    def delete(self, request, domain_id):
        try:
            DomainService.delete_domain(
                admin_id=str(request.user.user_id),
                domain_id=domain_id,
                ip_address=get_client_ip(request)
            )
            return api_success(data=None, status_code=204)
        except NotFoundError as e:
            return api_error('NOT_FOUND', str(e), status_code=404)

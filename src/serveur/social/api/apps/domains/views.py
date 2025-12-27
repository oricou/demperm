"""
Views for domains app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.domain_service import DomainService
from common.permissions import IsAuthenticated, IsNotBanned
from apps.custom_auth.authentication import FirebaseAuthentication
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ValidationError
from common.utils import get_client_ip
from .serializers import DomainSerializer, SubforumSerializer, CreateSubforumSerializer


class DomainsListView(APIView):
    """Get all domains."""
    # Use token-based Firebase authentication for these endpoints so that
    # unauthenticated requests are handled uniformly (no Session/CSRF).
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get all 9 fixed political domains",
        responses={200: DomainSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        """Get all domains."""
        # Manual authentication enforcement: tests expect 401 for unauthenticated
        if not (hasattr(request, 'firebase_uid') or (request.user and getattr(request.user, 'is_authenticated', False))):
            return Response({'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required'}}, status=status.HTTP_401_UNAUTHORIZED)
        domains = DomainService.get_all_domains()
        
        data = [{
            'domain_id': str(domain.domain_id),
            'name': domain.name,
            'description': domain.description,
            'created_at': domain.created_at
        } for domain in domains]
        
        return Response(data, status=status.HTTP_200_OK)


class DomainDetailView(APIView):
    """Get domain details."""
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get domain details",
        responses={200: DomainSerializer}
    )
    @rate_limit_general
    def get(self, request, domain_id):
        """Get domain."""
        # Manual authentication enforcement: tests expect 401 for unauthenticated
        if not (hasattr(request, 'firebase_uid') or (request.user and getattr(request.user, 'is_authenticated', False))):
            return Response({'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required'}}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            domain = DomainService.get_domain_by_id(domain_id)
            
            return Response({
                'domain_id': str(domain.domain_id),
                'name': domain.name,
                'description': domain.description,
                'created_at': domain.created_at
            }, status=status.HTTP_200_OK)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )


class DomainSubforumsView(APIView):
    """Get subforums for a domain."""
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get subforums for a domain",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: SubforumSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request, domain_id):
        """Get domain subforums."""
        # Manual auth enforcement for tests
        if not (hasattr(request, 'firebase_uid') or (request.user and getattr(request.user, 'is_authenticated', False))):
            return Response({'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required'}}, status=status.HTTP_401_UNAUTHORIZED)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        subforums = DomainService.get_domain_subforums(domain_id, page, page_size)
        
        data = [{
            'subforum_id': str(subforum.subforum_id),
            'name': subforum.name,
            'description': subforum.description,
            'parent_domain_id': str(subforum.parent_domain_id) if subforum.parent_domain_id else None,
            'created_at': subforum.created_at
        } for subforum in subforums]
        
        return Response(data, status=status.HTTP_200_OK)


class CreateDomainSubforumView(APIView):
    """Create a subforum in a domain."""
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Create a subforum in a domain",
        request_body=CreateSubforumSerializer,
        responses={201: SubforumSerializer}
    )
    @rate_limit_general
    def post(self, request, domain_id):
        """Create subforum."""
        # Manual auth enforcement for tests
        if not (hasattr(request, 'firebase_uid') or (request.user and getattr(request.user, 'is_authenticated', False))):
            return Response({'error': {'code': 'UNAUTHORIZED', 'message': 'Authentication required'}}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreateSubforumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            ip_address = get_client_ip(request)
            subforum = DomainService.create_subforum_in_domain(
                user_id=str(request.user.user_id),
                domain_id=domain_id,
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                ip_address=ip_address
            )
            
            return Response({
                'subforum_id': str(subforum.subforum_id),
                'name': subforum.subforum_name,
                'description': subforum.description,
                'parent_domain_id': str(subforum.parent_domain_id),
                'created_at': subforum.created_at
            }, status=status.HTTP_201_CREATED)
        except (ValidationError, NotFoundError) as e:
            return Response(
                {'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


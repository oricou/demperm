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
from common.exceptions import NotFoundError, ValidationError, ConflictError, PermissionDeniedError
from django.db import IntegrityError
from common.utils import get_client_ip
from .serializers import ForumSerializer, CreateForumSerializer
from db.repositories.domain_repository import SubforumRepository
from db.repositories.message_repository import AuditLogRepository
from services.apps_services.domain_service import DomainService
from common.validators import Validator
from django.db import transaction
from apps.domains.serializers import CreateSubforumSerializer, SubforumSerializer
from db.entities.domain_entity import Subforum


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
        except PermissionDeniedError as e:
            return Response(
                {'error': {'code': getattr(e, 'code', 'PERMISSION_DENIED'), 'message': str(getattr(e, 'message', e))}},
                status=getattr(e, 'status_code', status.HTTP_403_FORBIDDEN)
            )


class UserForumsView(APIView):
    """Get forums the authenticated user is a member of."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get forums for the authenticated user",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: ForumSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        memberships = ForumService.get_user_forums(str(request.user.user_id), page, page_size)

        data = []
        for m in memberships:
            forum = m.forum
            name = getattr(forum, 'name', None) or getattr(forum, 'forum_name', None)
            data.append({
                'forum_id': str(forum.forum_id),
                'name': name,
                'description': forum.description,
                'creator_id': str(forum.creator_id) if getattr(forum, 'creator_id', None) else None,
                'member_count': forum.member_count,
                'post_count': forum.post_count,
                'joined_at': m.joined_at
            })

        return Response(data, status=status.HTTP_200_OK)


class ForumSubforumsView(APIView):
    """List subforums under a forum."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get subforums for a forum",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: SubforumSerializer(many=True)}
    )
    @rate_limit_general
    def get(self, request, forum_id):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        try:
            ForumService.get_forum_by_id(forum_id)
        except NotFoundError as e:
            return Response({'error': {'code': 'NOT_FOUND', 'message': str(e)}}, status=status.HTTP_404_NOT_FOUND)

        subforums = SubforumRepository.get_by_forum(forum_id, page, page_size)

        data = [{
            'forum_id': str(s.forum_id_id),
            'subforum_id': str(s.subforum_id),
            'name': s.name,
            'description': s.description,
            'parent_forum_id': str(s.parent_forum_id) if s.parent_forum_id else None,
            'post_count': s.post_count,
            'created_at': s.created_at
        } for s in subforums]

        return Response(data, status=status.HTTP_200_OK)


class ForumTreeView(APIView):
    """Return a tree of subforums for a forum.

    Query params:
    - `depth` (int, optional): maximum depth to return. Root subforums are depth=1.
      If omitted, returns the full tree.
    """

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Get subforum tree for a forum",
        manual_parameters=[
            openapi.Parameter('depth', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Maximum depth (>=1)')
        ],
        responses={200: openapi.Response('Tree', SubforumSerializer(many=True))}
    )
    @rate_limit_general
    def get(self, request, forum_id):
        # ensure forum exists
        try:
            ForumService.get_forum_by_id(forum_id)
        except NotFoundError as e:
            return Response({'error': {'code': 'NOT_FOUND', 'message': str(e)}}, status=status.HTTP_404_NOT_FOUND)

        depth_param = request.query_params.get('depth')
        try:
            max_depth = int(depth_param) if depth_param is not None else None
            if max_depth is not None and max_depth < 1:
                raise ValueError()
        except ValueError:
            return Response({'error': {'code': 'VALIDATION_ERROR', 'message': 'Invalid depth parameter'}}, status=status.HTTP_400_BAD_REQUEST)

        # fetch top-level subforums for this forum (parent_forum_id == forum_id)
        roots = Subforum.objects.filter(parent_forum_id=forum_id).order_by('created_at')

        def build_node(s: Subforum, current_depth: int):
            node = {
                'subforum_id': str(s.subforum_id),
                'name': s.name,
                'description': s.description,
                'post_count': s.post_count,
                'created_at': s.created_at,
                'children': []
            }

            # stop if reached max depth
            if max_depth is not None and current_depth >= max_depth:
                return node

            # gather children by treating a subforum's forum as the parent forum
            # of nested subforums. When a subforum S has its own `forum_id` (a
            # Forum record created for the subforum), nested subforums created
            # under S will have `parent_forum_id == S.forum_id`. Therefore we
            # find those subforums and treat them as children here.
            children = Subforum.objects.filter(parent_forum_id=s.forum_id).order_by('created_at')

            node['children'] = [build_node(child, current_depth + 1) for child in children]

            return node

        tree = [build_node(r, 1) for r in roots]

        return Response(tree, status=status.HTTP_200_OK)


class CreateForumSubforumView(APIView):
    """Create a subforum under a forum."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(
        operation_description="Create a subforum under a forum",
        request_body=CreateSubforumSerializer,
        responses={201: SubforumSerializer}
    )
    @rate_limit_general
    @transaction.atomic
    def post(self, request, forum_id):
        serializer = CreateSubforumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # ensure forum exists
            ForumService.get_forum_by_id(forum_id)

            # validate fields consistently
            name = Validator.validate_forum_name(serializer.validated_data['name'])
            description = Validator.validate_description(serializer.validated_data['description'])

            parent_subforum_id = serializer.validated_data.get('parent_subforum_id')

            if parent_subforum_id:
                # validate parent exists and belongs to the same forum
                parent = SubforumRepository.get_by_id(parent_subforum_id)
                if not parent:
                    return Response({'error': {'code': 'VALIDATION_ERROR', 'message': f'Parent subforum {parent_subforum_id} not found'}}, status=status.HTTP_400_BAD_REQUEST)
                # parent must belong to this forum (cannot nest under a subforum for another forum)
                if not parent.forum_id_id or str(parent.forum_id_id) != str(forum_id):
                    return Response({'error': {'code': 'VALIDATION_ERROR', 'message': 'Parent subforum does not belong to this forum'}}, status=status.HTTP_400_BAD_REQUEST)

                # create nested subforum under the given parent
                subforum = ForumService.create_subforum_in_subforum(
                    user_id=str(request.user.user_id),
                    parent_subforum_id=str(parent_subforum_id),
                    name=name,
                    description=description,
                    ip_address=get_client_ip(request)
                )
            else:
                subforum = SubforumRepository.create(
                    creator_id=str(request.user.user_id),
                    subforum_name=name,
                    description=description,
                    parent_domain_id=None,
                    parent_forum_id=forum_id
                )

            # Audit
            ip_address = get_client_ip(request)
            AuditLogRepository.create(
                user_id=str(request.user.user_id),
                action_type='subforum_created',
                resource_type='subforum',
                resource_id=str(subforum.subforum_id),
                details={'forum_id': forum_id},
                ip_address=ip_address
            )

            return Response({
                'forum_id': str(subforum.forum_id_id),
                'subforum_id': str(subforum.subforum_id),
                'name': subforum.name,
                'description': subforum.description,
                'parent_forum_id': str(subforum.parent_forum_id) if subforum.parent_forum_id else None,
                'created_at': subforum.created_at
            }, status=status.HTTP_201_CREATED)
        except (ValidationError, NotFoundError) as e:
            return Response({'error': {'code': 'VALIDATION_ERROR', 'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        except ConflictError as e:
            return Response({'error': {'code': 'CONFLICT', 'message': str(e)}}, status=status.HTTP_409_CONFLICT)
        except IntegrityError as e:
            # Defensive: convert DB integrity errors to a conflict response
            return Response({'error': {'code': 'CONFLICT', 'message': 'Resource conflict while creating subforum'}}, status=status.HTTP_409_CONFLICT)


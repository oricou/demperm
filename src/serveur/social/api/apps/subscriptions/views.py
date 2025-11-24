"""
Views for subscriptions app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from services.apps_services.forum_service import ForumService
from services.apps_services.domain_service import DomainService
from db.repositories.domain_repository import SubforumSubscriptionRepository
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_general
from common.exceptions import NotFoundError, ConflictError
from common.utils import get_client_ip


class SubscribeForumView(APIView):
    """Subscribe to a forum (join)."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(operation_description="Subscribe to a forum")
    @rate_limit_general
    def post(self, request, forum_id):
        try:
            ip_address = get_client_ip(request)
            ForumService.join_forum(str(request.user.user_id), forum_id, ip_address)
            return Response({'message': 'Subscribed to forum'}, status=status.HTTP_201_CREATED)
        except (NotFoundError, ConflictError) as e:
            return Response({'error': {'code': 'ERROR', 'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeForumView(APIView):
    """Unsubscribe from a forum (leave)."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(operation_description="Unsubscribe from a forum")
    @rate_limit_general
    def delete(self, request, forum_id):
        try:
            ip_address = get_client_ip(request)
            ForumService.leave_forum(str(request.user.user_id), forum_id, ip_address)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response({'error': {'code': 'NOT_FOUND', 'message': str(e)}}, status=status.HTTP_404_NOT_FOUND)


class SubscribeSubforumView(APIView):
    """Subscribe to a subforum."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(operation_description="Subscribe to a subforum")
    @rate_limit_general
    def post(self, request, subforum_id):
        try:
            # Ensure subforum exists
            subforum = DomainService.get_subforum_by_id(subforum_id)

            if SubforumSubscriptionRepository.exists(str(request.user.user_id), subforum_id):
                raise ConflictError("Already subscribed to this subforum")

            SubforumSubscriptionRepository.create(str(request.user.user_id), subforum_id)
            return Response({'message': 'Subscribed to subforum'}, status=status.HTTP_201_CREATED)
        except (NotFoundError, ConflictError) as e:
            return Response({'error': {'code': 'ERROR', 'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeSubforumView(APIView):
    """Unsubscribe from a subforum."""

    permission_classes = [IsAuthenticated, IsNotBanned]

    @swagger_auto_schema(operation_description="Unsubscribe from a subforum")
    @rate_limit_general
    def delete(self, request, subforum_id):
        try:
            if not SubforumSubscriptionRepository.exists(str(request.user.user_id), subforum_id):
                raise NotFoundError("Not subscribed to this subforum")

            SubforumSubscriptionRepository.delete(str(request.user.user_id), subforum_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response({'error': {'code': 'NOT_FOUND', 'message': str(e)}}, status=status.HTTP_404_NOT_FOUND)

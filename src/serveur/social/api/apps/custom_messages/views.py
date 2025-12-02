"""
Views for messages app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.apps_services.message_service import MessageService
from common.permissions import IsAuthenticated, IsNotBanned
from common.rate_limiters import rate_limit_message_send
from common.exceptions import NotFoundError, ValidationError, PermissionDeniedError
from common.utils import get_client_ip
from .serializers import SendMessageSerializer, MessageSerializer, ConversationSerializer


class ConversationsListView(APIView):
    """Get all conversations."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get all conversations",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: ConversationSerializer(many=True)}
    )
    @rate_limit_message_send
    def get(self, request):
        """Get conversations."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        conversations = MessageService.get_conversations(str(request.user.user_id), page, page_size)
        
        # Serialize last_message objects
        for conv in conversations:
            if 'last_message' in conv and conv['last_message']:
                msg = conv['last_message']
                conv['last_message'] = {
                    'message_id': str(msg.message_id),
                    'sender_id': str(msg.sender_id),
                    'receiver_id': str(msg.receiver_id),
                    'encrypted_content': msg.encrypted_content,
                    'is_read': msg.is_read,
                    'created_at': msg.created_at.isoformat()
                }
        
        return Response(conversations, status=status.HTTP_200_OK)


class ConversationView(APIView):
    """Get conversation with a specific user."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Get conversation with a user",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=20)
        ],
        responses={200: MessageSerializer(many=True)}
    )
    @rate_limit_message_send
    def get(self, request, user_id):
        """Get conversation."""
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        messages = MessageService.get_conversation(str(request.user.user_id), user_id, page, page_size)
        
        data = [{
            'message_id': str(msg.message_id),
            'sender_id': str(msg.sender_id),
            'receiver_id': str(msg.receiver_id),
            'encrypted_content': msg.encrypted_content,
            'encryption_key_sender': msg.encryption_key_sender,
            'encryption_key_receiver': msg.encryption_key_receiver,
            'is_read': msg.is_read,
            'created_at': msg.created_at
        } for msg in messages]
        
        return Response(data, status=status.HTTP_200_OK)


class SendMessageView(APIView):
    """Send a message to a user."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Send an E2E encrypted message",
        request_body=SendMessageSerializer,
        responses={201: MessageSerializer}
    )
    @rate_limit_message_send
    def post(self, request, user_id):
        """Send message."""
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            ip_address = get_client_ip(request)
            message = MessageService.send_message(
                sender_id=str(request.user.user_id),
                receiver_id=user_id,
                content=serializer.validated_data['content'],
                sender_public_key=serializer.validated_data['sender_public_key'],
                receiver_public_key=serializer.validated_data['receiver_public_key'],
                ip_address=ip_address
            )
            
            return Response({
                'message_id': str(message.message_id),
                'sender_id': str(message.sender_id),
                'receiver_id': str(message.receiver_id),
                'encrypted_content': message.encrypted_content,
                'encryption_key_sender': message.encryption_key_sender,
                'encryption_key_receiver': message.encryption_key_receiver,
                'is_read': message.is_read,
                'created_at': message.created_at
            }, status=status.HTTP_201_CREATED)
        except (ValidationError, NotFoundError) as e:
            return Response(
                {'error': {'code': 'ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class DeleteConversationView(APIView):
    """Delete a conversation with a specific user."""
    
    permission_classes = [IsAuthenticated, IsNotBanned]
    
    @swagger_auto_schema(
        operation_description="Delete conversation with a user (soft delete)",
        responses={
            204: openapi.Response(description="Conversation deleted"),
            404: openapi.Response(description="User not found"),
            400: openapi.Response(description="Bad request")
        }
    )
    def delete(self, request, user_id):
        """Delete conversation."""
        try:
            ip_address = get_client_ip(request)
            MessageService.delete_conversation(
                user_id=str(request.user.user_id),
                other_user_id=user_id,
                ip_address=ip_address
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFoundError as e:
            return Response(
                {'error': {'code': 'NOT_FOUND', 'message': str(e)}},
                status=status.HTTP_404_NOT_FOUND
            )
        except (ValidationError, PermissionDeniedError) as e:
            return Response(
                {'error': {'code': 'ERROR', 'message': str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


"""
URL configuration for messages app.
"""
from django.urls import path
from .views import ConversationsListView, ConversationView, SendMessageView, DeleteConversationView

app_name = 'messages'

urlpatterns = [
    # Conversations
    path('', ConversationsListView.as_view(), name='conversations-list'),
    path('<str:user_id>/', ConversationView.as_view(), name='conversation'),
    path('<str:user_id>/create/', SendMessageView.as_view(), name='send-message'),
    path('<str:user_id>/delete/', DeleteConversationView.as_view(), name='delete-conversation'),
]


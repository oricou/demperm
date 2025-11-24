"""
URL configuration for messages app.
"""
from django.urls import path
from .views import ConversationsListView, ConversationView, SendMessageView

app_name = 'messages'

urlpatterns = [
    # Conversations
    path('', ConversationsListView.as_view(), name='conversations-list'),
    path('<str:user_id>/', ConversationView.as_view(), name='conversation'),
    path('<str:user_id>/send/', SendMessageView.as_view(), name='send-message'),
]


"""
URL configuration for subscriptions app.
"""
from django.urls import path
from .views import (
    SubscribeForumView, UnsubscribeForumView,
    SubscribeSubforumView, UnsubscribeSubforumView
)

app_name = 'subscriptions'

urlpatterns = [
    path('forums/<str:forum_id>/', SubscribeForumView.as_view(), name='subscribe-forum'),
    path('forums/<str:forum_id>/unsubscribe/', UnsubscribeForumView.as_view(), name='unsubscribe-forum'),
    path('subforums/<str:subforum_id>/', SubscribeSubforumView.as_view(), name='subscribe-subforum'),
    path('subforums/<str:subforum_id>/unsubscribe/', UnsubscribeSubforumView.as_view(), name='unsubscribe-subforum'),
]

"""
URL configuration for followers app.
"""
from django.urls import path
from .views import (
    FollowUserView, UnfollowUserView, AcceptFollowRequestView,
    RejectFollowRequestView, FollowersListView, FollowingListView,
    PendingRequestsView
)

app_name = 'followers'

urlpatterns = [
    # Current user's followers/following
    path('me/followers/', FollowersListView.as_view(), name='my-followers'),
    path('me/following/', FollowingListView.as_view(), name='my-following'),
    path('me/pending/', PendingRequestsView.as_view(), name='pending-requests'),
    
    # Follow operations
    path('<str:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<str:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('<str:user_id>/accept/', AcceptFollowRequestView.as_view(), name='accept-request'),
    path('<str:user_id>/reject/', RejectFollowRequestView.as_view(), name='reject-request'),
]


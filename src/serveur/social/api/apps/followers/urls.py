"""
URL configuration for followers app.
"""
from django.urls import path
from .views import (
    FollowUserView, UnfollowUserView, AcceptFollowRequestView,
    RefuseFollowRequestView, FollowersListView, FollowingListView,
    PendingRequestsView
)

app_name = 'followers'

urlpatterns = [
    # Current user's followers/following
    path('me/', FollowersListView.as_view(), name='my-followers'),
    path('following/', FollowingListView.as_view(), name='my-following'),
    path('pending/', PendingRequestsView.as_view(), name='pending-requests'),
    
    # Follow operations
    path('<str:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<str:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('<str:user_id>/accept/', AcceptFollowRequestView.as_view(), name='accept-request'),
    path('<str:user_id>/refuse/', RefuseFollowRequestView.as_view(), name='refuse-request'),
]


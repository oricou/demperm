"""
URL configuration for users app.
"""
from django.urls import path
from .views import (
    CurrentUserView, UpdateCurrentUserView, UpdateCurrentUserSettingsView,
    UserDetailView, BlockUserView, UnblockUserView, BlockedUsersView,
    UserSearchView, UserBulkView
)

app_name = 'users'

urlpatterns = [
    # Current user
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('me/update/', UpdateCurrentUserView.as_view(), name='update-profile'),
    path('me/settings/', UpdateCurrentUserSettingsView.as_view(), name='update-settings'),
    path('me/blocked/', BlockedUsersView.as_view(), name='blocked-users'),
    
    # User operations
    path('search/', UserSearchView.as_view(), name='search-users'),
    path('bulk/', UserBulkView.as_view(), name='bulk-users'),
    
    # Specific user
    path('<str:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('<str:user_id>/block/', BlockUserView.as_view(), name='block-user'),
    path('<str:user_id>/unblock/', UnblockUserView.as_view(), name='unblock-user'),
]


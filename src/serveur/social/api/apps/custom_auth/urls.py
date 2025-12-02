"""
URL configuration for auth app.
"""
from django.urls import path
from .views import (
    GoogleAuthURLView,
    GoogleAuthCallbackView,
    TokenRefreshView,
    LogoutView,
)

app_name = 'custom_auth'

urlpatterns = [
    path('google/url/', GoogleAuthURLView.as_view(), name='google-auth-url'),
    path('google/callback/', GoogleAuthCallbackView.as_view(), name='google-callback'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


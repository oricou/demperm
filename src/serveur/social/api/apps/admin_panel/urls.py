"""
URL configuration for admin_panel app.
"""
from django.urls import path
from .views import ReportsListView, UpdateReportStatusView, BanUserView, UnbanUserView

app_name = 'admin_panel'

urlpatterns = [
    # Reports management
    path('reports/', ReportsListView.as_view(), name='reports-list'),
    path('reports/<str:report_id>/resolve/', UpdateReportStatusView.as_view(), name='update-report'),
    
    # User moderation
    path('users/<str:user_id>/ban/', BanUserView.as_view(), name='ban-user'),
    path('users/<str:user_id>/unban/', UnbanUserView.as_view(), name='unban-user'),
]


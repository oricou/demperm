"""
URL configuration for reports app.
"""
from django.urls import path
from .views import CreateReportView

app_name = 'reports'

urlpatterns = [
    path('create/', CreateReportView.as_view(), name='create-report'),
]


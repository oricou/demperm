"""
URL configuration for subforums app.
"""
from django.urls import path
from .views import SubforumDetailView, SubforumPostsView

app_name = 'subforums'

urlpatterns = [
    path('<str:subforum_id>/', SubforumDetailView.as_view(), name='subforum-detail'),
    path('<str:subforum_id>/posts/', SubforumPostsView.as_view(), name='subforum-posts'),
]

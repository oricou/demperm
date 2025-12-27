"""
URL configuration for posts app.
"""
from django.urls import path
from .views import (
    CreatePostView, PostDetailView, DeletePostView,
    LikePostView, UnlikePostView, PostLikesView,
    MyPostsView, FeedView, DiscoverView
)

app_name = 'posts'

urlpatterns = [
    # Post operations
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('me/', MyPostsView.as_view(), name='my-posts'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('discover/', DiscoverView.as_view(), name='discover'),
    
    # Specific post
    path('<str:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('<str:post_id>/delete/', DeletePostView.as_view(), name='delete-post'),
    path('<str:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('<str:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('<str:post_id>/likes/', PostLikesView.as_view(), name='post-likes'),
]


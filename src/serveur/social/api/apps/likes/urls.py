"""
URL configuration for likes app.
"""
from django.urls import path
from .views import LikePostView, UnlikePostView, PostLikesView

app_name = 'likes'

urlpatterns = [
    path('posts/<str:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<str:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('posts/<str:post_id>/likes/', PostLikesView.as_view(), name='post-likes'),
]

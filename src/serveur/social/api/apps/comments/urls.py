"""
URL configuration for comments app.
"""
from django.urls import path
from .views import (
    PostCommentsView, CreateCommentView, DeleteCommentView, CommentRepliesView
)

app_name = 'comments'

urlpatterns = [
    # Post comments
    path('posts/<str:post_id>/', PostCommentsView.as_view(), name='post-comments'),
    path('posts/<str:post_id>/create/', CreateCommentView.as_view(), name='create-comment'),
    
    # Comment operations
    path('<str:comment_id>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
    path('<str:comment_id>/replies/', CommentRepliesView.as_view(), name='comment-replies'),
]


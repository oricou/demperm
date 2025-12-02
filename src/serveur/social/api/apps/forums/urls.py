"""
URL configuration for forums app.
"""
from django.urls import path
from .views import (
    ForumsListView, CreateForumView, ForumDetailView,
    SearchForumsView, JoinForumView, LeaveForumView,
    UserForumsView, ForumSubforumsView, CreateForumSubforumView
)

app_name = 'forums'

urlpatterns = [
    # Forums
    path('', ForumsListView.as_view(), name='forums-list'),
    path('create/', CreateForumView.as_view(), name='create-forum'),
    path('search/', SearchForumsView.as_view(), name='search-forums'),
    path('me/', UserForumsView.as_view(), name='forums-me'),
    
    # Specific forum
    path('<str:forum_id>/', ForumDetailView.as_view(), name='forum-detail'),
    path('<str:forum_id>/subforums/', ForumSubforumsView.as_view(), name='forum-subforums'),
    path('<str:forum_id>/subforums/create/', CreateForumSubforumView.as_view(), name='create-forum-subforum'),
    path('<str:forum_id>/join/', JoinForumView.as_view(), name='join-forum'),
    path('<str:forum_id>/leave/', LeaveForumView.as_view(), name='leave-forum'),
]


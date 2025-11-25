"""
URL configuration for tags app.
"""
from django.urls import path
from .views import (
    TagsListView, CreateTagView, DeleteTagView,
    AssignTagsView, UnassignTagsView
)

app_name = 'tags'

urlpatterns = [
    path('', TagsListView.as_view(), name='tags-list'),
    path('create/', CreateTagView.as_view(), name='create-tag'),
    path('<str:tag_id>/delete/', DeleteTagView.as_view(), name='delete-tag'),
    path('assign/<str:post_id>/', AssignTagsView.as_view(), name='assign-tags'),
    path('unassign/<str:post_id>/', UnassignTagsView.as_view(), name='unassign-tags'),
]

"""
URL configuration for admin_panel app.
"""
from django.urls import path
from .views_reports import ReportsListView, ResolveReportView, RejectReportView
from .views_moderation import BanUserView, UnbanUserView, RemovePostView, RemoveCommentView
from .views_domains import AdminDomainCreateView, AdminDomainUpdateView
from .views_tags import DeleteTagView
from .views_stats import UsersStatsView, PostsStatsView, ActivityStatsView

app_name = 'admin_panel'

urlpatterns = [
    # Reports management
    path('reports/', ReportsListView.as_view(), name='reports-list'),
    path('reports/<str:report_id>/resolve/', ResolveReportView.as_view(), name='resolve-report'),
    path('reports/<str:report_id>/reject/', RejectReportView.as_view(), name='reject-report'),
    
    # User moderation
    path('users/<str:user_id>/ban/', BanUserView.as_view(), name='ban-user'),
    path('users/<str:user_id>/unban/', UnbanUserView.as_view(), name='unban-user'),

    # Domains management
    path('domains/create/', AdminDomainCreateView.as_view(), name='create-domain'),
    path('domains/<str:domain_id>/', AdminDomainUpdateView.as_view(), name='update-domain'),

    # Tags management
    path('tags/delete/', DeleteTagView.as_view(), name='delete-tag'),

    # Content moderation
    path('posts/<str:post_id>/remove/', RemovePostView.as_view(), name='remove-post'),
    path('comments/<str:comment_id>/remove/', RemoveCommentView.as_view(), name='remove-comment'),

    # Stats
    path('stats/users/', UsersStatsView.as_view(), name='stats-users'),
    path('stats/posts/', PostsStatsView.as_view(), name='stats-posts'),
    path('stats/activity/', ActivityStatsView.as_view(), name='stats-activity'),
]


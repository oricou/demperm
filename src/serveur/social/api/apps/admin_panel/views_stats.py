"""
Admin panel views for statistics.
"""
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from common.permissions import IsAuthenticated, IsAdmin
from common.rate_limiters import rate_limit_general
from db.entities.user_entity import User
from db.entities.post_entity import Post, Comment
from db.entities.message_entity import Report
from .serializers import StatsUsersSerializer, StatsPostsSerializer, StatsActivitySerializer
from .response_utils import api_success


class UsersStatsView(APIView):
    """User stats (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="User statistics",
        responses={200: StatsUsersSerializer}
    )
    @rate_limit_general
    def get(self, request):
        today = timezone.now().date()
        start_week = today - timedelta(days=7)
        total_users = User.objects.count()
        new_users_today = User.objects.filter(created_at__date=today).count()
        new_users_this_week = User.objects.filter(created_at__date__gte=start_week).count()
        active_users_today = User.objects.filter(last_login_at__date=today).count()
        banned_users = User.objects.filter(is_banned=True).count()
        return api_success(
            data={
                'total_users': total_users,
                'new_users_today': new_users_today,
                'new_users_this_week': new_users_this_week,
                'active_users_today': active_users_today,
                'banned_users': banned_users,
            },
            status_code=200
        )


class PostsStatsView(APIView):
    """Post stats (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Post statistics",
        responses={200: StatsPostsSerializer}
    )
    @rate_limit_general
    def get(self, request):
        today = timezone.now().date()
        start_week = today - timedelta(days=7)
        total_posts = Post.objects.count()
        new_posts_today = Post.objects.filter(created_at__date=today).count()
        new_posts_this_week = Post.objects.filter(created_at__date__gte=start_week).count()
        total_comments = Comment.objects.count()
        return api_success(
            data={
                'total_posts': total_posts,
                'new_posts_today': new_posts_today,
                'new_posts_this_week': new_posts_this_week,
                'total_comments': total_comments,
            },
            status_code=200
        )


class ActivityStatsView(APIView):
    """Global activity stats (admin only)."""

    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Activity statistics",
        responses={200: StatsActivitySerializer}
    )
    @rate_limit_general
    def get(self, request):
        total_reports = Report.objects.count()
        pending_reports = Report.objects.filter(status='pending').count()
        resolved_reports = Report.objects.filter(status='resolved').count()
        rejected_reports = Report.objects.filter(status='rejected').count()
        return api_success(
            data={
                'total_reports': total_reports,
                'pending_reports': pending_reports,
                'resolved_reports': resolved_reports,
                'rejected_reports': rejected_reports,
            },
            status_code=200
        )

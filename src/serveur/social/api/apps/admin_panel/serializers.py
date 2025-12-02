"""
Serializers for admin_panel app.
"""
from rest_framework import serializers


class UpdateReportStatusSerializer(serializers.Serializer):
    """Serializer for updating report status."""
    status = serializers.ChoiceField(choices=['resolved', 'rejected'])


class ReportSerializer(serializers.Serializer):
    """Serializer for report."""
    report_id = serializers.UUIDField(read_only=True)
    reporter = serializers.DictField(read_only=True)
    target_type = serializers.CharField(read_only=True)
    target_id = serializers.UUIDField(read_only=True)
    target_preview = serializers.DictField(read_only=True, required=False)
    reason = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True, allow_null=True)
    status = serializers.CharField(read_only=True)
    resolved_by = serializers.UUIDField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    resolved_at = serializers.DateTimeField(read_only=True, allow_null=True)
    
    class Meta:
        # Explicit ref_name avoids collisions with other serializers that
        # share the same class name in different modules when drf_yasg
        # generates component $ref names.
        ref_name = 'AdminReportSerializer'


class DomainCreateUpdateSerializer(serializers.Serializer):
    """Serializer for creating/updating domains (admin)."""
    domain_name = serializers.CharField(required=True, min_length=3, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    icon_url = serializers.CharField(required=False, allow_blank=True, max_length=500)

    class Meta:
        ref_name = 'AdminDomainCreateUpdateSerializer'


class StatsUsersSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    new_users_today = serializers.IntegerField()
    new_users_this_week = serializers.IntegerField()
    active_users_today = serializers.IntegerField()
    banned_users = serializers.IntegerField()

    class Meta:
        ref_name = 'AdminUsersStatsSerializer'


class StatsPostsSerializer(serializers.Serializer):
    total_posts = serializers.IntegerField()
    new_posts_today = serializers.IntegerField()
    new_posts_this_week = serializers.IntegerField()
    total_comments = serializers.IntegerField()

    class Meta:
        ref_name = 'AdminPostsStatsSerializer'


class StatsActivitySerializer(serializers.Serializer):
    total_reports = serializers.IntegerField()
    pending_reports = serializers.IntegerField()
    resolved_reports = serializers.IntegerField()
    rejected_reports = serializers.IntegerField()

    class Meta:
        ref_name = 'AdminActivityStatsSerializer'


class ReportActionSerializer(serializers.Serializer):
    """Serializer for resolving/rejecting a report."""
    action_taken = serializers.CharField(required=False, allow_blank=True, max_length=200)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=500)

    class Meta:
        ref_name = 'AdminReportActionSerializer'


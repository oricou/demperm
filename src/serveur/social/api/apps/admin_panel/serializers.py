"""
Serializers for admin_panel app.
"""
from rest_framework import serializers


class UpdateReportStatusSerializer(serializers.Serializer):
    """Serializer for updating report status."""
    status = serializers.ChoiceField(choices=['under_review', 'resolved', 'rejected'])


class ReportSerializer(serializers.Serializer):
    """Serializer for report."""
    report_id = serializers.UUIDField(read_only=True)
    reporter_id = serializers.UUIDField(read_only=True)
    target_type = serializers.CharField(read_only=True)
    target_id = serializers.UUIDField(read_only=True)
    reason = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    resolved_at = serializers.DateTimeField(read_only=True, allow_null=True)
    
    class Meta:
        # Explicit ref_name avoids collisions with other serializers that
        # share the same class name in different modules when drf_yasg
        # generates component $ref names.
        ref_name = 'AdminReportSerializer'


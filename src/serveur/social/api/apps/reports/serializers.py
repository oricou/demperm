"""
Serializers for reports app.
"""
from rest_framework import serializers


class CreateReportSerializer(serializers.Serializer):
    """Serializer for creating a report."""
    target_type = serializers.ChoiceField(choices=['post', 'comment', 'user'])
    target_id = serializers.UUIDField()
    reason = serializers.CharField(max_length=500)


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
        # Unique ref_name to avoid collision with the admin_panel.ReportSerializer
        ref_name = 'ReportsReportSerializer'


from rest_framework import serializers


class ThresholdSettingSerializer(serializers.Serializer):
    userId = serializers.CharField()
    threshold = serializers.IntegerField()

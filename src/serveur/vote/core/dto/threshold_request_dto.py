from rest_framework import serializers


class ThresholdUpdateRequestSerializer(serializers.Serializer):
    threshold = serializers.IntegerField(min_value=0)

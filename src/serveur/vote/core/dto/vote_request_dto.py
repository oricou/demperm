from rest_framework import serializers

class VoteRequestSerializer(serializers.Serializer):
    targetUserId = serializers.CharField()
    domain = serializers.CharField(max_length=100)

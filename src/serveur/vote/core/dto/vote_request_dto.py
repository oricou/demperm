from rest_framework import serializers

class VoteRequestSerializer(serializers.Serializer):
    targetUserId = serializers.UUIDField()
    domain = serializers.CharField(max_length=100)

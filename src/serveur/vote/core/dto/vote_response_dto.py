from rest_framework import serializers

class VoteSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    voterId = serializers.UUIDField()
    targetUserId = serializers.UUIDField()
    domain = serializers.CharField(max_length=100)
    createdAt = serializers.DateTimeField()

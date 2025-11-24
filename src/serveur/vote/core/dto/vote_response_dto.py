from rest_framework import serializers


class VoteSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    voterId = serializers.UUIDField()
    targetUserId = serializers.UUIDField()
    domain = serializers.CharField()
    createdAt = serializers.DateTimeField()


class ReceivedVotesSerializer(serializers.Serializer):
    userId = serializers.UUIDField()
    total = serializers.IntegerField()
    byDomain = serializers.DictField(
        child=serializers.IntegerField(),
    )
    usersByDomain = serializers.DictField(
        child=serializers.ListField(
            child=serializers.UUIDField()
        )
    )

from rest_framework import serializers


class VoteSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    voterId = serializers.CharField()
    targetUserId = serializers.CharField()
    domain = serializers.CharField()
    createdAt = serializers.DateTimeField()


class ReceivedVotesSerializer(serializers.Serializer):
    userId = serializers.CharField()
    total = serializers.IntegerField()
    byDomain = serializers.DictField(
        child=serializers.IntegerField(),
    )
    usersByDomain = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField()
        )
    )

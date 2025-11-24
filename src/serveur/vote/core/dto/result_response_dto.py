from rest_framework import serializers


class VoteResultSerializer(serializers.Serializer):
    """
    DTO pour la réponse de l'endpoint /results.
    Correspond au schéma VoteResult du Swagger.
    """
    userId = serializers.CharField()
    domain = serializers.CharField()
    count = serializers.IntegerField()
    elected = serializers.BooleanField()
    electedAt = serializers.DateTimeField(allow_null=True, required=False)

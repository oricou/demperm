from rest_framework import serializers


class PublicationSettingSerializer(serializers.Serializer):
    """
    DTO pour la réponse des endpoints de publication.
    Correspond au schéma PublicationSetting du Swagger.
    """
    userId = serializers.CharField()
    publishVotes = serializers.BooleanField()

from rest_framework import serializers


class PublicationUpdateRequestSerializer(serializers.Serializer):
    """
    DTO pour la mise à jour des préférences de publication.
    Correspond au body du PUT /publication/{userId}
    """
    publishVotes = serializers.BooleanField()
    threshold = serializers.IntegerField(min_value=-1)

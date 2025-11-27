from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.dto.publication_request_dto import PublicationUpdateRequestSerializer
from core.dto.publication_response_dto import PublicationSettingSerializer
from core.services.publication_service import PublicationService


class PublicationSettingView(APIView):
    """
    GET /publication/{userId}
    Récupère les paramètres de publication d'un utilisateur.
    200: PublicationSetting avec userId et publishVotes
    401: Non autorisé
    
    PUT /publication/{userId}
    Met à jour les paramètres de publication d'un utilisateur.
    request.data: {"publishVotes": bool}
    200: PublicationSetting mis à jour
    400: Requête invalide
    401: Non autorisé
    403: Interdit (si l'utilisateur tente de modifier un autre compte)
    """

    def get(self, request, userId):
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        if current_user_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        setting = PublicationService.get_publication_setting(userId)
        response_serializer = PublicationSettingSerializer(setting)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, userId):
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        if current_user_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if str(current_user_id) != str(userId):
            return Response(
                {"error": "Forbidden: You can only modify your own publication settings"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PublicationUpdateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        publish_votes = serializer.validated_data["publishVotes"]
        updated_setting = PublicationService.update_publication_setting(
            userId, publish_votes
        )

        response_serializer = PublicationSettingSerializer(updated_setting)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)

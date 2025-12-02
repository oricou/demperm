from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.dto.publication_request_dto import PublicationUpdateRequestSerializer
from core.dto.publication_response_dto import PublicationSettingSerializer
from core.services.publication_service import PublicationService


class PublicationSettingView(APIView):
    """
    GET /api/publication
    PUT /api/publication
    """

    @extend_schema(
        tags=["Preferences"],
        responses={
            200: PublicationSettingSerializer,
            403: OpenApiResponse(description="Unauthorized"),
        },
        description="Récupère les paramètres de publication d’un utilisateur.",
    )
    def get(self, request):
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        setting = PublicationService.get_publication_setting(current_user_id)
        response_serializer = PublicationSettingSerializer(setting)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Preferences"],
        request=PublicationUpdateRequestSerializer,
        responses={
            200: PublicationSettingSerializer,
            400: OpenApiResponse(description="Requête invalide"),
            403: OpenApiResponse(description="Unauthorized"),
        },
        description=(
            "L'utilisateur accepte ou refuse la publication automatique de son nombre de"
            "voix / votes et active une valeur max de voix qu'il peut recevoir (-1 => pas de limite)."
        ),
    )
    def put(self, request):
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        serializer = PublicationUpdateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        publish_votes = serializer.validated_data["publishVotes"]
        threshold = serializer.validated_data["threshold"]
        updated_setting = PublicationService.update_publication_setting(
            current_user_id, publish_votes, threshold
        )

        response_serializer = PublicationSettingSerializer(updated_setting)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)

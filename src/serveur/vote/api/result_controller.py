from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from core.dto.result_response_dto import VoteResultSerializer
from core.services.result_service import ResultService


class ResultView(APIView):
    """
    GET /results
    Récupère les résultats des votes avec classement.
    
    Query params:
    - domain (optionnel): Filtrer par domaine
    - top (optionnel, défaut 100): Nombre de résultats à retourner
    - since (optionnel): Date au format YYYY-MM-DD pour filtrer les votes depuis cette date
    
    Réponse 200: Liste de VoteResult
    Réponse 400: Paramètres invalides
    Réponse 401: Non autorisé
    """

    def get(self, request):
        """
        Récupère les résultats agrégés des votes.
        """
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        if current_user_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Récupération des paramètres query
        domain = request.query_params.get("domain", None)
        top = request.query_params.get("top", 100)
        since_str = request.query_params.get("since", None)

        # Validation de 'top'
        try:
            top = int(top)
            if top <= 0:
                return Response(
                    {"error": "Parameter 'top' must be a positive integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Parameter 'top' must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validation de 'since'
        since = None
        if since_str:
            try:
                since = datetime.strptime(since_str, "%Y-%m-%d")
            except ValueError:
                return Response(
                    {"error": "Parameter 'since' must be in YYYY-MM-DD format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Récupération des résultats
        results = ResultService.get_vote_results(
            domain=domain,
            top=top,
            since=since
        )

        # Sérialisation
        serializer = VoteResultSerializer(results, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

from typing import Dict
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.dto.stats_response_dto import StatsDailySerializer, StatsMonthlySerializer, StatsChartSerializer
from core.services.stats_service import StatsService

class StatsDailyView(APIView):
    """
    GET /stats/votes/daily/{userId}
    Récupère le nombre de votes qu'un utilisateur a reçu pour chaque jour (histogramme)
    """

    @extend_schema(
        tags=["Statistics"],
        parameters=[
            OpenApiParameter(name="userId", location=OpenApiParameter.PATH, required=True, type=str, description="Id de l'utilisateur"),
            OpenApiParameter(name="days", location=OpenApiParameter.QUERY, required=False, type=int, description="Nombre de jours à retourner", default=30),
            OpenApiParameter(name="includeMonthly", location=OpenApiParameter.QUERY, required=False, type=bool, description="Inclure aussi les données mensuelles", default=False),
        ],
        responses={200: StatsDailySerializer, 401: OpenApiResponse(description="Unauthorized")},
        description="Retourne les votes reçus par jour par domaine."
    )
    def get(self, request, userId: str):
        if getattr(request.user, "id", None) is None:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        days = int(request.query_params.get("days", 30))
        include_monthly = request.query_params.get("includeMonthly", "false").lower() in ("1", "true", "yes")

        res = StatsService.get_daily_stats(userId, days=days, include_monthly=include_monthly)
        by_domain = res.get("byDomain", [])  # list of {domain, series:[{date,count},...]}
        print(by_domain)
        payload = {
            "userId": res.get("userId", userId),
            "byDomain": by_domain,
            "monthlyByDomain": res.get("monthlyByDomain")
        }
        serializer = StatsDailySerializer(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatsMonthlyView(APIView):
    """
    GET /stats/votes/monthly/{userId}
    Récupère le nombre de votes qu'un utilisateur a reçu pour chaque mois (histogramme)
    """

    @extend_schema(
        tags=["Statistics"],
        parameters=[
            OpenApiParameter(name="userId", location=OpenApiParameter.PATH, required=True, type=str, description="Id de l'utilisateur"),
            OpenApiParameter(name="months", location=OpenApiParameter.QUERY, required=False, type=int, description="Nombre de mois à retourner", default=12),
        ],
        responses={200: StatsMonthlySerializer, 401: OpenApiResponse(description="Unauthorized")},
        description="Retourne la série mensuelle par domaine."
    )
    def get(self, request, userId: str):
        current_user_id = getattr(request.user, "id", None)
        if current_user_id is None:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        months = int(request.query_params.get("months", 12))
        monthly_by_domain = StatsService.get_monthly_stats(userId, months=months)

        payload = {"userId": userId, "monthlyByDomain": monthly_by_domain}
        serializer = StatsMonthlySerializer(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StatsChartView(APIView):
    """
    GET /stats/chart
    Récupère les 10 utilisateurs les plus votés pour chaque domaine, ainsi qu'un histogramme de votes pour chacun d'eux.
    """

    @extend_schema(
        tags=["Statistics"],
        parameters=[
            OpenApiParameter(name="domain", location=OpenApiParameter.QUERY, required=False, type=str, description="Filtrer par domaine"),
            OpenApiParameter(name="days", location=OpenApiParameter.QUERY, required=False, type=int, description="Période en jours", default=30),
        ],
        responses={200: StatsChartSerializer(many=True), 401: OpenApiResponse(description="Unauthorized")},
        description="Retourne les données des scores des 10 utilisateurs avec le plus de voix par domaine sur les derniers jours."
    )
    def get(self, request):
        current_user_id = getattr(request.user, "id", None)
        if current_user_id is None:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        domain = request.query_params.get("domain")
        days = int(request.query_params.get("days", 30))

        chart = StatsService.get_chart(domain=domain, days=days)
        serializer = StatsChartSerializer(data=chart, many=True)
        serializer.is_valid(raise_exception=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

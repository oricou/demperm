from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.dto.stats_response_dto import StatsDailySerializer, StatsMonthlySerializer, StatsChartSerializer
from core.services.stats_service import StatsService

from datetime import date

class StatsDailyView(APIView):
    """
    GET /stats/votes/daily/{userId}
    Récupère le nombre de votes qu'un utilisateur a reçu pour chaque jour (histogramme)
    200: Nombre de votes reçus pour chaque jour
    404: Not found
    """

    def get(self, request, userId):
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        if current_user_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        res = StatsService.get_daily_stats(current_user_id)
        print(res)
        delta = res[0]['count'] if res[0]['date'] == date.today() else 0
        response_serializer = StatsDailySerializer({
            'userId': current_user_id,
            'daily': res,
            'delta': delta
        })
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class StatsMonthlyView(APIView):
    """
    GET /stats/votes/monthly/{userId}
    Récupère le nombre de votes qu'un utilisateur a reçu pour chaque mois (histogramme)
    200: Nombre de votes reçus pour chaque mois
    404: Not found
    """

    def get(self, request, userId):
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        if current_user_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        res = StatsService.get_monthly_stats(current_user_id)
        print(res)
        today = date.today()
        delta = res[0]['count'] if res[0]['year'] == today.year and res[0]['month'] == today.month else 0
        response_serializer = StatsMonthlySerializer({
            'userId': current_user_id,
            'monthly': res,
            'delta': delta
        })
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class StatsChartView(APIView):
    """
    GET /stats/chart
    Récupère les 10 utilisateurs les plus votés pour chaque domaine, ainsi qu'un histogramme de votes pour chacun d'eux.
    200: Le chart
    404: Not found
    """

    def get(self, request):
        user = getattr(request, "user", None)
        current_user_id = getattr(user, "id", None)

        if current_user_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        res = StatsService.get_chart()
        print(res)
        response_serializer = StatsChartSerializer(data=res, many=True)
        response_serializer.is_valid()
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)

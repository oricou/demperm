from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.dto.vote_request_dto import VoteRequestSerializer
from core.dto.vote_response_dto import VoteSerializer, ReceivedVotesSerializer
from core.services.vote_service import VoteService
from core.services.vote_validation_service import VoteValidationService


class VoteView(APIView):
    """
    POST /api/votes
    """

    @extend_schema(
        tags=["Votes"],
        request=VoteRequestSerializer,
        responses={
            201: VoteSerializer,
            400: OpenApiResponse(description="Invalid payload"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        description="Crée un vote pour un domaine donné."
    )
    def post(self, request):
        serializer = VoteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = getattr(request, "user", None)
        voter_id = getattr(user, "id", None)

        if voter_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = serializer.validated_data

        vote_dict = VoteService.create_vote(
            voter_id=str(voter_id),
            target_user_id=str(data["targetUserId"]),
            domain=data["domain"],
        )

        response_serializer = VoteSerializer(vote_dict)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class VoteDeleteView(APIView):
    """
    DELETE /api/votes/{domain}
    """

    @extend_schema(
        tags=["Votes"],
        parameters=[
            OpenApiParameter(
                name="domain",
                type=str,
                location=OpenApiParameter.PATH,
                description="Domaine du vote à supprimer",
            )
        ],
        responses={
            204: OpenApiResponse(description="Vote supprimé"),
            404: OpenApiResponse(description="Vote introuvable"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        description="Supprime le vote de l'utilisateur authentifié pour un domaine."
    )
    def delete(self, request, domain: str):
        user = getattr(request, "user", None)
        voter_id = getattr(user, "id", None)

        if voter_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        deleted = VoteService.delete_vote(
            voter_id=str(voter_id),
            domain=domain,
        )

        if not deleted:
            return Response(
                {"error": "Vote not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class VotesByVoterView(APIView):
    """
    GET /api/votes/by-user/{userId}
    """

    @extend_schema(
        tags=["Votes"],
        parameters=[
            OpenApiParameter(
                name="voterId",
                type=str,
                location=OpenApiParameter.PATH,
                description="ID de l'utilisateur dont on veut les votes",
            ),
            OpenApiParameter(
                name="domain",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtrer par domaine",
            )
        ],
        responses={200: VoteSerializer(many=True)},
        description="Retourne la liste des votes effectués par un utilisateur donné."
    )
    def get(self, request, voterId: str):
        user = getattr(request, "user", None)
        if getattr(user, "id", None) is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        domain = request.query_params.get("domain")

        votes = VoteService.get_votes_by_voter(
            voter_id=str(voterId),
            domain=domain,
        )

        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VotesByVoterMeView(APIView):
    """
    GET /api/votes/by-voter/me
    """
    
    @extend_schema(
        tags=["Votes"],
        parameters=[
            OpenApiParameter(
                name="domain",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtrer par domaine",
            )
        ],
        responses={200: VoteSerializer(many=True)},
        description="Retourne la liste des votes effectués par l'utilisateur authentifié."
    )
    def get(self, request):
        user = getattr(request, "user", None)
        voter_id = getattr(user, "id", None)

        if voter_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        domain = request.query_params.get("domain")

        votes = VoteService.get_votes_by_voter(
            voter_id=str(voter_id),
            domain=domain,
        )

        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VotesForUserView(APIView):
    """
    GET /api/votes/for-user/{userId}
    """

    @extend_schema(
        tags=["Votes"],
        parameters=[
            OpenApiParameter(
                name="userId",
                type=str,
                location=OpenApiParameter.PATH,
                description="Utilisateur dont on veut les votes reçus"
            ),
            OpenApiParameter(
                name="domain",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtrer par domaine"
            )
        ],
        responses={200: ReceivedVotesSerializer},
        description="Retourne les votes reçus par un utilisateur."
    )
    def get(self, request, userId: str):
        user = getattr(request, "user", None)
        if getattr(user, "id", None) is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        domain = request.query_params.get("domain")

        received_votes = VoteService.get_received_votes(
            user_id=str(userId),
            domain=domain,
        )

        serializer = ReceivedVotesSerializer(received_votes)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VotesForUserMeView(APIView):
    """
    GET /api/votes/for-user/me
    """
    
    @extend_schema(
        tags=["Votes"],
        parameters=[
            OpenApiParameter(
                name="domain",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtrer par domaine"
            )
        ],
        responses={200: ReceivedVotesSerializer},
        description="Retourne les votes reçus par l'utilisateur authentifié."
    )
    def get(self, request):
        user = getattr(request, "user", None)
        user_id = getattr(user, "id", None)

        if user_id is None:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        domain = request.query_params.get("domain")

        received_votes = VoteService.get_received_votes(
            user_id=str(user_id),
            domain=domain,
        )

        serializer = ReceivedVotesSerializer(received_votes)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VoteValidationView(APIView):
    """
    GET /api/votes/validate/force
    """
    
    @extend_schema(
        tags=["Votes"],
        responses={200: OpenApiResponse(description="Validation exécutée")},
        description="Force l'exécution de la tâche quotidienne de validation des votes."
    )
    def get(self):
        VoteValidationService.process_daily_votes()
        return Response(status=status.HTTP_200_OK)

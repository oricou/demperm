from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.dto.vote_request_dto import VoteRequestSerializer
from core.dto.vote_response_dto import VoteSerializer, ReceivedVotesSerializer
from core.services.vote_service import VoteService


class VoteView(APIView):
    """
    POST /votes
    Body: VoteRequest
    Réponse 201: Vote

    DELETE /votes/{domain}
    Réponse 204: OK
    Réponse 404: Vote introuvable
    """

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

    def delete(self, request, domain: str):
        """
        DELETE /votes/{domain}
        Supprime le vote de l'utilisateur authentifié pour un domaine donné.
        """
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
    GET /votes/by-voter/{voterId}?domain=xxx
    Retourne la liste des votes effectués par un utilisateur donné.
    """

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
    GET /votes/by-voter/me?domain=xxx
    Retourne la liste des votes effectués par l'utilisateur authentifié.
    """

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
    GET /votes/for-user/{userId}?domain=xxx
    Retourne les votes reçus par un utilisateur (total + par domaine + électeurs).
    """

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
    GET /votes/for-user/me?domain=xxx
    Retourne les votes reçus par l'utilisateur authentifié.
    """

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

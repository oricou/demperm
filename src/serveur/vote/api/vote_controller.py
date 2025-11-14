from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.dto.vote_request_dto import VoteRequestSerializer
from core.dto.vote_response_dto import VoteSerializer
from core.services.vote_service import VoteService

class VoteView(APIView):
    """
    POST /votes
    Body: VoteRequest
    Réponse 201: Vote
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

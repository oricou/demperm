import uuid
from django.utils import timezone

from db.repository.vote_repository import VoteRepository


class VoteService:
    @staticmethod
    def create_vote(voter_id: str, target_user_id: str, domain: str) -> dict:
        """
        Crée un vote + le persiste dans Neo4j, puis renvoie un dict
        """
        vote = {
            "id": uuid.uuid4(),
            "voterId": voter_id,
            "targetUserId": target_user_id,
            "domain": domain,
            "createdAt": timezone.now(),
        }

        VoteRepository.save_vote(vote)

        return vote

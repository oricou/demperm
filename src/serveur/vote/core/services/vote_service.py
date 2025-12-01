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

    @staticmethod
    def delete_vote(voter_id: str, domain: str) -> bool:
        """
        Supprime le vote d'un utilisateur pour un domaine donné.
        Retourne True si quelque chose a été supprimé, False sinon.
        """
        return VoteRepository.delete_vote_for_voter_and_domain(
            voter_id=voter_id,
            domain=domain,
        )

    @staticmethod
    def get_votes_by_voter(voter_id: str, domain: str | None = None) -> list[dict]:
        """
        Récupère la liste des votes émis par un user (option: filtrer par domaine).
        """
        return VoteRepository.find_votes_by_voter(
            voter_id=voter_id,
            domain=domain,
        )

    @staticmethod
    def get_received_votes(user_id: str, domain: str | None = None) -> dict:
        """
        Récupère les votes reçus par un user :
        {
          "userId": str,
          "total": int,
          "byDomain": { str: int },
          "usersByDomain": { str: [str] }
        }
        """
        return VoteRepository.get_received_votes_summary(
            user_id=user_id,
            domain=domain,
        )

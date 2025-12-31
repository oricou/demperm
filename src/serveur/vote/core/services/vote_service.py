import os
import uuid
from django.utils import timezone

from db.repository.vote_repository import VoteRepository

MIN_PUBLIC_VOTES = int(os.getenv("MIN_PUBLIC_VOTES", 5))

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
    def get_votes_by_voter(voter_id: str, domain: str | None = None, is_me: bool = False) -> list[dict]:
        """
        Récupère la liste des votes émis par un user (option: filtrer par domaine).
        """
        
        publish_votes, stats = VoteRepository.get_publish_votes_setting(voter_id)
        last_update = VoteRepository.get_last_update()
        last_counts = stats[last_update] if last_update in stats else {}
        public_domains = set()
        if is_me or publish_votes:
            public_domains = set(VoteRepository.get_all_domains())
        else:
            for domain_name, count in last_counts.items():
                if count >= MIN_PUBLIC_VOTES:
                    public_domains.add(domain_name)
    

        votes = VoteRepository.find_votes_by_voter(
            voter_id=voter_id,
            domain=domain,
        )
        return [vote_entry for vote_entry in votes if vote_entry["domain"] in public_domains]

    @staticmethod
    def get_received_votes(user_id: str, domain: str | None = None, is_me: bool = False) -> dict:
        """
        Récupère les votes reçus par un user :
        {
          "userId": str,
          "total": int,
          "byDomain": { str: int },
          "usersByDomain": { str: [str] }
        }
        """

        publish_votes, stats = VoteRepository.get_publish_votes_setting(user_id)
        last_update = VoteRepository.get_last_update()
        last_counts = stats[last_update] if last_update in stats else {}
        public_domains = set()

        for domain_name, count in last_counts.items():
            if is_me or publish_votes or count >= MIN_PUBLIC_VOTES:
                public_domains.add(domain_name)

        res = VoteRepository.get_received_votes_summary(
            user_id=user_id,
            domain=domain,
        )

        res["byDomain"] = {
            domain_key: count
            for domain_key, count in last_counts.items()
            if domain_key in public_domains
        }
        res["usersByDomain"] = {
            domain_key: [
                voter_id
                for voter_id in voter_ids
            ]
            for domain_key, voter_ids in res["usersByDomain"].items()
            if domain_key in public_domains
        }
        res["total"] = sum(res["byDomain"].values())
        return res

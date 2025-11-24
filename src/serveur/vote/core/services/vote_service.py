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
    def remove_previous_votes():
        """
        Supprime les votes en double par domaine, puis recalcule les poids des votes.
        
        Étapes :  
        1. Supprime les relations VOTED en doublon pour chaque utilisateur et chaque domaine.  
        2. Recalcule les poids (`count`) et marque les cycles (`cycle`) pour tous les votes valides  
           via le recalcul par domaine dans GDS.  
        """
        VoteRepository.clean_duplicate_domain_votes()

        VoteRepository.recalculate_counts_by_domain()

import random
from db.repository.vote_repository import VoteRepository
from core.services.vote_service import VoteService

class VoteValidationService:
    @staticmethod
    def process_daily_votes():
        """
        Traite les votes non encore validés chaque jour :
        - Supprime ou réinitialise les votes précédents via le service VoteService
        - Récupère les IDs des relations VOTED non traitées dans la base Neo4j
        - Mélange aléatoirement ces votes
        - Valide environ 80 % des votes et rejette les 20 % restants
        - Marque les votes validés ou invalidés dans Neo4j via VoteRepository
        """
        
        # Supprimer ou réinitialiser les votes précédents (logique métier externe)
        VoteService.remove_previous_votes()

        # Récupérer la liste des relations VOTED non encore traitées
        vote_ids = VoteRepository.fetch_unprocessed_votes()

        # Si aucun vote à traiter, on sort
        if not vote_ids:
            return
        
        # Mélanger les IDs pour éviter un biais d'ordre
        random.shuffle(vote_ids)
        # Déterminer le nombre de votes à valider (80 %)
        cutoff = int(len(vote_ids) * 0.8)

        # Séparer les votes validés et rejetés
        validated = vote_ids[:cutoff]
        rejected = vote_ids[cutoff:]

        # TODO: ajouter la logique de validité d'un vote sur validated

        # Marquer les votes validés dans la base
        if validated:
            VoteRepository.mark_votes_valid(validated)

        # Marquer les votes rejetés dans la base
        if rejected:
            VoteRepository.mark_votes_invalid(rejected)

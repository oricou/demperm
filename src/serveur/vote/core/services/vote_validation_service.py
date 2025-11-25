import random
from db.repository.vote_repository import VoteRepository

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

        # Supprimer ou réinitialiser les votes précédents
        VoteValidationService.remove_previous_votes()

        # Récupérer la liste des relations VOTED non encore traitées
        vote_ids = VoteRepository.fetch_unprocessed_votes()

        # Si aucun vote à traiter, on sort
        if not vote_ids:
            return
        
        # Mélanger les IDs pour éviter un biais d'ordre
        random.shuffle(vote_ids)
        # Déterminer le nombre de votes à valider (80 %)
        cutoff = int(len(vote_ids) * 0.8) + 1

        # Séparer les votes validés et rejetés
        validated = vote_ids[:cutoff]
        rejected = vote_ids[cutoff:]

        # Logique de validation des votes de validated
        for vote_id in validated:
            if not VoteValidationService.validate_vote(vote_id):
                rejected.append(vote_id)

        # Marquer les votes rejetés dans la base
        if rejected:
            VoteRepository.mark_votes_invalid(rejected)

    @staticmethod
    def remove_previous_votes():
        """
        Supprime les votes en double par domaine, puis recalcule les poids des votes.
        
        Étapes :
        1. Supprime les relations VOTED en doublon et valide toutes les self-loop pour chaque
           utilisateur et chaque domaine.
        2. Recalcule les poids (`count`) et marque les cycles (`cycle`) pour tous les votes valides
           via le recalcul par domaine dans GDS.
        """
        VoteRepository.clean_duplicate_domain_votes()

        VoteRepository.recalculate_counts_by_domain()
    
    @staticmethod
    def validate_vote(vote_id: str) -> bool:
        """
        Valide un vote en vérifiant sa légitimité selon les seuils et les relations.

        :param vote_id: l’ID (elementId) de la relation VOTED à valider  
        :return: True si le vote est validé (processed = true et valid = true), False si invalidé  
        """ 
        (count, rel_ids, cycle) = VoteRepository.check_vote_validity(vote_id)

        if (count == -1):
            return False
        
        VoteRepository.mark_vote_valid(vote_id)
        VoteRepository.update_counts(vote_id, count, rel_ids, cycle)

        return True
        
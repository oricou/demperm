from typing import Optional, List
from datetime import datetime

from db.repository.result_repository import ResultRepository


class ResultService:
    """
    Service pour la gestion des résultats de votes.
    """

    # Seuil minimum pour être élu (membre du Conseil municipal)
    # Conforme à la page 12 du document : "20% des voix dans son domaine"
    ELECTION_THRESHOLD = 0.20  # 20%

    @staticmethod
    def get_vote_results(
        domain: Optional[str] = None,
        top: int = 100,
        since: Optional[datetime] = None
    ) -> List[dict]:
        """
        Récupère les résultats agrégés des votes.
        
        Args:
            domain: Domaine optionnel pour filtrer les votes
            top: Nombre maximum de résultats (défaut: 100)
            since: Date optionnelle - votes depuis cette date
            
        Returns:
            Liste de résultats avec userId, domain, count, elected, electedAt
        """
        # Récupérer les résultats du repository (qui incluent domainTotal)
        results = ResultRepository.get_vote_results(domain, top, since)
        
        # Calculer elected pour chaque résultat
        # elected = true si votes >= 20% des votes du domaine
        for result in results:
            domain_total = result.get('domainTotal', 0)
            
            if domain_total > 0:
                # Élu si au moins 20% des voix du domaine
                result['elected'] = (result['count'] >= domain_total * ResultService.ELECTION_THRESHOLD)
            else:
                # Si pas de total (cas impossible), considérer comme non élu
                result['elected'] = False
            
            # Retirer domainTotal des résultats (usage interne uniquement)
            result.pop('domainTotal', None)
        
        return results
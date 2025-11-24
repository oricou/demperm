from app.neo4j_config import get_driver
from datetime import datetime
from typing import Optional, List


class ResultRepository:
    """
    Repository pour récupérer les résultats agrégés des votes.
    
    Récupère le classement des utilisateurs par nombre de votes reçus,
    avec filtrage optionnel par domaine et date.
    """

    @staticmethod
    def get_vote_results(
        domain: Optional[str] = None,
        top: int = 100,
        since: Optional[datetime] = None
    ) -> List[dict]:
        """
        Récupère les résultats des votes agrégés.
        
        Args:
            domain: Domaine optionnel pour filtrer les votes
            top: Nombre maximum de résultats à retourner (défaut: 100)
            since: Date optionnelle - ne retourner que les votes depuis cette date
            
        Returns:
            Liste de dict contenant userId, domain, count, elected, electedAt
        """
        driver = get_driver()
        with driver.session() as session:
            results = session.execute_read(
                ResultRepository._get_vote_results_tx,
                domain,
                top,
                since
            )
            return results

    @staticmethod
    def _get_vote_results_tx(
        tx,
        domain: Optional[str],
        top: int,
        since: Optional[datetime]
    ) -> List[dict]:
        """
        Transaction de lecture pour récupérer les résultats agrégés.
        
        Cette fonction utilise 2 requêtes pour éviter le bug du calcul
        des 20% avec le paramètre top :
        1. Calcul des totaux par domaine (sur TOUS les votes)
        2. Récupération des top N candidats avec leur domainTotal
        """
        
        # Paramètres communs
        params = {"top": top}
        conditions = []
        
        if domain:
            conditions.append("v.domain = $domain")
            params["domain"] = domain
        
        if since:
            conditions.append("v.createdAt >= datetime($since)")
            params["since"] = since.isoformat()
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # ═══════════════════════════════════════════════════════════════
        # REQUÊTE 1 : Calculer les totaux par domaine
        # ═══════════════════════════════════════════════════════════════
        query_totals = f"""
            MATCH (voter:User)-[v:VOTED]->(target:User)
            {where_clause}
            RETURN v.domain AS domain, sum(v.count) AS domainTotal
        """
        
        result_totals = tx.run(query_totals, **params)
        domain_totals = {record["domain"]: record["domainTotal"] for record in result_totals}
        
        # ═══════════════════════════════════════════════════════════════
        # REQUÊTE 2 : Récupérer les top N candidats
        # ═══════════════════════════════════════════════════════════════
        query_results = f"""
            MATCH (voter:User)-[v:VOTED]->(target:User)
            {where_clause}
            WITH target.id AS userId,
                 v.domain AS domain,
                 sum(v.count) AS userVotes,
                 min(v.createdAt) AS firstVoteAt
            ORDER BY userVotes DESC
            LIMIT $top
            RETURN userId, domain, userVotes AS count, firstVoteAt AS electedAt
        """
        
        result_users = tx.run(query_results, **params)
        
        # Construire les résultats avec le domainTotal
        results = []
        for record in result_users:
            user_domain = record["domain"]
            results.append({
                "userId": record["userId"],
                "domain": user_domain,
                "count": record["count"],
                "domainTotal": domain_totals.get(user_domain, 0),
                "electedAt": record["electedAt"]
            })
        
        return results
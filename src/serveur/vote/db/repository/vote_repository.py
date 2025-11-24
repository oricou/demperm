from app.neo4j_config import get_driver

class VoteRepository:
    """
    Persistance des votes dans Neo4j.

    Modèle :
      (voter:User {id})
          -[:VOTED {id, createdAt, domain, count, processed, valid, cycle}]->
      (target:User {id})
    """

    @staticmethod
    def save_vote(vote: dict) -> None:
        """
        vote = {
          "id": uuid,
          "voterId": str,
          "targetUserId": str,
          "domain": str,
          "createdAt": datetime
        }
        """
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(VoteRepository._save_vote_tx, vote)

    @staticmethod
    def _save_vote_tx(tx, vote: dict):
        tx.run(
            """
            MERGE (voter:User {id: $voterId})
            MERGE (target:User {id: $targetUserId})

            WITH voter, target

            OPTIONAL MATCH (voter)<-[incoming:VOTED]-()
            WITH voter, target,
                CASE
                    WHEN coalesce(sum(incoming.count), 0) = 0
                    THEN 1
                    ELSE coalesce(sum(incoming.count), 0)
                END AS voteWeight

            MERGE (voter)-[rel:VOTED {domain: $domain}]->(target)
            ON CREATE SET
                rel.id        = $id,
                rel.createdAt = datetime($createdAt),
                rel.count     = voteWeight,
                rel.processed = false,
                rel.valid     = null
            ON MATCH SET
                rel.count     = rel.count + voteWeight,
                rel.processed = false,
                rel.valid     = null
            """,
            id=str(vote["id"]),
            voterId=str(vote["voterId"]),
            targetUserId=str(vote["targetUserId"]),
            domain=vote["domain"],
            createdAt=vote["createdAt"].isoformat(),
        )


    # -------------------- RECUPERATION DES VOTES NON TRAITES --------------------
    
    @staticmethod
    def fetch_unprocessed_votes():
        """
        Récupère les relations VOTED dont processed = false (votes non traités).
        Retourne une liste d'elementId() des relations.
        """
        driver = get_driver()
        with driver.session() as session:
            results = session.execute_read(
                VoteRepository._fetch_unprocessed_votes_tx
            )
            return results

    @staticmethod
    def _fetch_unprocessed_votes_tx(tx):
        # Sélectionne toutes les relations VOTED non encore traitées
        results = tx.run(
            """
            MATCH ()-[v:VOTED]-()
            WHERE coalesce(v.processed, false) = false
            RETURN elementId(v) as relId
            """
        ).data()
        
        # Retourne uniquement les identifiants des relations
        return [row["relId"] for row in results]


    # -------------------- MARQUAGE DES VOTES VALIDES --------------------

    @staticmethod
    def mark_votes_valid(rel_ids: list):
        """
        Marque une liste de relations VOTED comme validées :
        processed = true et valid = true.
        """
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(
                VoteRepository._mark_votes_valid_tx, rel_ids
            )

    @staticmethod
    def _mark_votes_valid_tx(tx, rel_ids):
        # Met à jour les propriétés processed et valid sur les relations
        tx.run(
            """
            MATCH ()-[v]-()
            WHERE elementId(v) IN $ids
            SET v.processed = true,
                v.valid = true
            """,
            ids=rel_ids,
        )


    # -------------------- MARQUAGE DES VOTES INVALIDES --------------------

    @staticmethod
    def mark_votes_invalid(rel_ids: list):
        """
        Marque une liste de relations VOTED comme invalidées :
        processed = true et valid = false.
        """
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(
                VoteRepository._mark_votes_invalid_tx, rel_ids
            )

    @staticmethod
    def _mark_votes_invalid_tx(tx, rel_ids):
        # Même logique que mark_votes_valid, mais valid = false
        tx.run(
            """
            MATCH ()-[v]-()
            WHERE elementId(v) IN $ids
            SET v.processed = true,
                v.valid = false
            """,
            ids=rel_ids,
        )
    

    # -------------------- SUPRESSION DES VOTES DUPLIQUES --------------------

    @staticmethod
    def clean_duplicate_domain_votes():
        """
        Supprime les votes en double pour un même utilisateur et un même domaine.
        Seul le plus récent est conservé.
        A utiliser pour supprimer les votes qui ont une copie non traitée.
        """
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(VoteRepository._clean_duplicate_domain_votes_tx)

    @staticmethod
    def _clean_duplicate_domain_votes_tx(tx):
        # Identifie les votes doublons par utilisateur + domaine,
        # trie par date, conserve le plus récent et supprime les autres.
        tx.run(
            """
            MATCH (voter:User)-[v:VOTED]->()
            WITH voter, v.domain AS domain, collect(v) AS votes

            WHERE size(votes) > 1
            UNWIND votes AS vote
            WITH voter, domain, vote
            ORDER BY vote.createdAt DESC
            WITH voter, domain, collect(vote) AS sortedVotes
            WITH voter, domain, head(sortedVotes) AS keep, tail(sortedVotes) AS toDelete
            FOREACH (v IN toDelete | DELETE v)
            """
        )


    # -------------------- RECALCUL GLOBAL DES COUNTS DES VOTES --------------------

    @staticmethod  
    def recalculate_counts_by_domain():  
        """
        Recalcule tous les poids des relations VOTED :
        - Réinitialisation globale
        - Recalcul domaine par domaine
        - Nettoyage final des graphes GDS
        """
        driver = get_driver()
        
        # 1. Phase d'initialisation + récupération des domaines existants
        with driver.session() as session:
            domains = session.execute_write(VoteRepository._setup_recalculation_by_domain_tx)

        # 2. Recalcul pour chaque domaine
        for domain in domains:
            with driver.session() as session:
                session.execute_write(VoteRepository._recalculate_counts_by_domain_tx, domain)

        # 3. Suppression du graphe global utilisé dans GDS
        with driver.session() as session:
            session.execute_write(VoteRepository._cleanup_recalculation_by_domain_tx)

    @staticmethod
    def _setup_recalculation_by_domain_tx(tx):
        # 1. Remise à zéro des propriétés `count` et `cycle` de toutes les relations VOTED
        tx.run("""
            MATCH ()-[r:VOTED]->()
            WHERE r.valid = true
            SET r.count = null, r.cycle = false
        """)

        # 2. Collecte de tous les domaines présents dans les relations VOTED
        result = tx.run("MATCH ()-[r:VOTED]->() RETURN DISTINCT r.domain AS domain")
        domains = [record["domain"] for record in result]

        # 3. Projection du graphe global dans GDS avec toutes les relations VOTED
        tx.run("""
            CALL gds.graph.project(
                'myGraph',
                'User',
                { VOTED: { type: 'VOTED', orientation: 'NATURAL' } }
            )
        """)

        # Retourner la liste des domaines pour itération
        return domains

    @staticmethod
    def _recalculate_counts_by_domain_tx(tx, domain):
        graph_name = f"myGraph_{domain}"

        # 4. Projection d'un sous-graphe GDS filtré par domaine
        #    On ne projette que les relations VOTED de ce domaine
        tx.run(
            """
            MATCH (u1:User)-[r:VOTED]->(u2:User)
            WHERE r.domain = $domain
            AND r.valid = true
            WITH u1, u2, type(r) AS relType
            RETURN gds.graph.project(
                $graphName,
                u1, u2,
                { relationshipType: relType }
            ) AS g
            """,
            domain=domain,
            graphName=graph_name
        )

        # 5. Calcul des composantes fortement connexes (SCC) dans ce sous-graphe
        tx.run(
            "CALL gds.scc.write($graphName, { writeProperty: 'component' })",
            graphName=graph_name
        )

        # 6. Marquage des relations cycliques (dans ce domaine) :
        #    celles dont les deux extrémités sont dans la même composante
        tx.run(
            """
            MATCH (u1:User)-[r:VOTED]->(u2:User)
            WHERE u1.component = u2.component
            AND r.domain = $domain
            AND r.valid = true
            SET r.cycle = true
            """,
            domain=domain
        )

        # 7. Tri topologique des nœuds dans ce sous-graphe (DAG)
        topo = tx.run(
            """
            CALL gds.dag.topologicalSort.stream(
                $graphName,
                { relationshipTypes: ['VOTED'], computeMaxDistanceFromSource: true }
            )
            YIELD nodeId, maxDistanceFromSource
            RETURN gds.util.asNode(nodeId).id AS businessId, maxDistanceFromSource
            ORDER BY maxDistanceFromSource
            """,
            graphName=graph_name
        ).data()

        # 8. Propagation des poids (count) hors cycle
        #    Pour chaque nœud selon l’ordre topologique, somme des entrantes + 1
        for rec in topo:
            businessId = rec["businessId"]
            incoming_rec = tx.run(
                """
                MATCH (src:User)-[inR:VOTED]->(u)
                WHERE u.id = $businessId
                AND inR.cycle = false
                AND inR.domain = $domain
                AND inR.valid = true
                RETURN sum(coalesce(inR.count, 0)) AS incoming
                """,
                businessId=businessId,
                domain=domain
            ).single()
            incoming = incoming_rec["incoming"] or 0

            tx.run(
                """
                MATCH (u:User)-[outR:VOTED]->(v)
                WHERE u.id = $businessId
                AND outR.cycle = false
                AND outR.domain = $domain
                AND outR.valid = true
                SET outR.count = $newCount
                """,
                businessId=businessId,
                domain=domain,
                newCount=1 + incoming
            )

        # 9. Calcul des poids des cycles :
        #    On trouve les composantes cycliques (taille > 1) et on calcule le “cycle value”
        comps = tx.run(
            """
            MATCH (u:User)
            WHERE EXISTS {
                MATCH (u)-[r:VOTED]->()
                WHERE r.domain = $domain
                AND r.valid = true
            }
            WITH u.component AS comp, count(*) AS compSize
            WHERE compSize > 1
            RETURN comp, compSize
            """,
            domain=domain
        ).data()

        for rec in comps:
            comp = rec["comp"]
            comp_size = rec["compSize"]

            ext_sum_rec = tx.run(
                """
                MATCH (src:User)-[r:VOTED]->(dst:User)
                WHERE dst.component = $comp
                AND src.component <> $comp
                AND r.domain = $domain
                AND r.valid = true
                RETURN sum(coalesce(r.count, 0)) AS extSum
                """,
                comp=comp,
                domain=domain
            ).single()
            ext_sum = ext_sum_rec["extSum"] or 0

            cycle_value = comp_size + ext_sum

            tx.run(
                """
                MATCH (a:User)-[rel:VOTED]->(b:User)
                WHERE a.component = $comp
                AND b.component = $comp
                AND rel.domain = $domain
                AND rel.valid = true
                SET rel.count = $cycleValue
                """,
                comp=comp,
                domain=domain,
                cycleValue=cycle_value
            )

        # 10. Nettoyage : suppression de la propriété component sur les nœuds User
        tx.run("MATCH (u:User) REMOVE u.component")

        # 11. Suppression du graphe GDS projeté pour ce domaine
        tx.run("CALL gds.graph.drop($graphName) YIELD graphName", graphName=graph_name)

    @staticmethod
    def _cleanup_recalculation_by_domain_tx(tx):
        # Supprime le graphe global projeté dans GDS
        tx.run("CALL gds.graph.drop('myGraph') YIELD graphName")

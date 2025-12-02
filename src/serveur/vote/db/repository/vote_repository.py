import datetime
from app.neo4j_config import get_driver
from uuid import *
from typing import List

class VoteRepository:
    """
    Persistance des votes dans Neo4j.

    Modèle :
      (voter:User {id, threshold, publishVotes})
          -[:VOTED {id, createdAt, domain, count, processed, valid, cycle, current}]->
      (target:User {id, threshold, publishVotes})
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
            MATCH (v:User {id: $voterId})-[rel:VOTED {domain: $domain, processed: false}]->(t:User)
            WHERE t.id <> $targetUserId
            DELETE rel
            """,
            voterId=str(vote["voterId"]),
            domain=vote["domain"],
            targetUserId=str(vote["targetUserId"]),
        )

        tx.run(
            """
            MERGE (voter:User {id: $voterId})
            ON CREATE SET
                voter.threshold    = 100,
                voter.publishVotes = false
            MERGE (target:User {id: $targetUserId})
            ON CREATE SET
                target.threshold    = 100,
                target.publishVotes = false

            WITH voter, target

            MERGE (voter)-[rel:VOTED {domain: $domain, processed: false}]->(target)
            ON CREATE SET
                rel.id        = $id,
                rel.createdAt = datetime($createdAt),
                rel.processed = false
            """,
            id=str(vote["id"]),
            voterId=str(vote["voterId"]),
            targetUserId=str(vote["targetUserId"]),
            domain=vote["domain"],
            createdAt=vote["createdAt"].isoformat(),
        )

    @staticmethod
    def delete_vote_for_voter_and_domain(voter_id: str, domain: str) -> bool:
        """
        Supprime la relation VOTED pour un voter + domain.
        Retourne True si une relation a été supprimée, False sinon.
        """
        driver = get_driver()
        with driver.session() as session:
            return session.execute_write(
                VoteRepository._delete_vote_for_voter_and_domain_tx,
                voter_id,
                domain,
            )

    @staticmethod
    def _delete_vote_for_voter_and_domain_tx(tx, voter_id: str, domain: str) -> bool:
        # Supprime les votes non processed qui ne font pas un self-loop et renvoie le nombre supprimé
        result = tx.run(
            """
            MATCH (v:User {id: $voterId})-[r:VOTED {domain: $domain}]->(t:User)
            WHERE (r.processed = false) AND t.id <> $voterId
            DELETE r
            RETURN count(r) AS nbDeleted
            """,
            voterId=voter_id,
            domain=domain,
        ).single()
        deleted_count = result["nbDeleted"] if result is not None else 0

        # Compte les votes self-loop et les votes self-loop non processed
        self_record = tx.run(
            """
            MATCH (v:User {id: $voterId})-[r:VOTED {domain: $domain}]->(v)
            RETURN count(r) AS selfCount,
                sum(CASE WHEN r.process = false THEN 1 ELSE 0 END) AS selfNotValidCount
            """,
            voterId=voter_id,
            domain=domain,
        ).single()
        self_count = self_record["selfCount"] or 0
        self_not_valid = self_record["selfNotValidCount"] or 0


        if self_not_valid == 0 and self_count == 0:
            # Compte les votes valide qui ne font pas un self-loop
            valid_not_self_record = tx.run(
                """
                MATCH (v:User {id: $voterId})-[r:VOTED {domain: $domain, valid: true}]->(t:User)
                RETURN count(r) AS relCount
                """,
                voterId=voter_id,
                domain=domain,
            ).single()
            rel_count = valid_not_self_record["relCount"] or 0

            # Créer une self-loop non processed
            tx.run(
                """
                MATCH (v:User {id: $voterId})
                MERGE (v)-[r:VOTED {domain: $domain}]->(v)
                SET r.processed = false,
                    r.createdAt = datetime($createdAt)
                """,
                voterId=voter_id,
                domain=domain,
                createdAt=datetime.datetime.now().isoformat()
            )

            # Renvoie False si on n'a supprimé aucun vote non valide
            # et qu'il n'y a aucun vote valide actuellement
            return not (rel_count == 0 and deleted_count == 0)
        
        return deleted_count > 0
        

    @staticmethod
    def find_votes_by_voter(voter_id: str, domain: str | None = None) -> list[dict]:
        driver = get_driver()
        with driver.session() as session:
            return session.execute_read(
                VoteRepository._find_votes_by_voter_tx,
                voter_id,
                domain,
            )

    @staticmethod
    def _find_votes_by_voter_tx(tx, voter_id: str, domain: str | None) -> list[dict]:
        query = """
            MATCH (voter:User {id: $voterId})-[rel:VOTED]->(target:User)
            WHERE $domain IS NULL OR rel.domain = $domain
            RETURN rel.id        AS id,
                   voter.id      AS voterId,
                   target.id     AS targetUserId,
                   rel.domain    AS domain,
                   rel.createdAt AS createdAt
            ORDER BY rel.createdAt DESC
            """

        records = tx.run(
            query,
            voterId=str(voter_id),
            domain=domain,
        )

        votes: list[dict] = []
        for record in records:
            created_at = record["createdAt"]
            if hasattr(created_at, "to_native"):
                created_at = created_at.to_native()

            votes.append(
                {
                    "id": record["id"],
                    "voterId": record["voterId"],
                    "targetUserId": record["targetUserId"],
                    "domain": record["domain"],
                    "createdAt": created_at,
                }
            )

        return votes

    @staticmethod
    def get_received_votes_summary(user_id: str, domain: str | None = None) -> dict:
        """
        Retourne un dict:
        {
          "userId": str,
          "total": int,
          "byDomain": { str: int },
          "usersByDomain": { str: [str] }
        }
        """
        driver = get_driver()
        with driver.session() as session:
            return session.execute_read(
                VoteRepository._get_received_votes_summary_tx,
                user_id,
                domain,
            )

    @staticmethod
    def _get_received_votes_summary_tx(tx, user_id: str, domain: str | None) -> dict:
        query = """
                MATCH (voter:User)-[rel:VOTED {processed: true, valid: true}]->(target:User {id: $userId})
                WHERE $domain IS NULL OR rel.domain = $domain
                RETURN rel.domain                 AS domain,
                       sum(rel.count)             AS count,
                       collect(DISTINCT voter.id) AS voters
            """

        records = tx.run(
            query,
            userId=str(user_id),
            domain=domain,
        )

        by_domain: dict[str, int] = {}
        users_by_domain: dict[str, list[str]] = {}
        total = 0

        for record in records:
            domain_key = record["domain"]
            if domain_key is None:
                continue

            count = record["count"] or 0
            voters = record["voters"] or []

            by_domain[domain_key] = int(count)
            users_by_domain[domain_key] = [str(v) for v in voters]
            total += int(count)

        return {
            "userId": str(user_id),
            "total": total,
            "byDomain": by_domain,
            "usersByDomain": users_by_domain,
        }


    # -------------------- RECUPERATION DES VOTES NON TRAITES --------------------
    
    @staticmethod
    def fetch_unprocessed_votes() -> list[str]:
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
    def _fetch_unprocessed_votes_tx(tx) -> list[str]:
        # Sélectionne toutes les relations VOTED non encore traitées
        results = tx.run(
            """
            MATCH (:User)-[v:VOTED]->(:User)
            WHERE coalesce(v.processed, false) = false
            RETURN elementId(v) as relId
            """
        ).data()
        
        # Retourne uniquement les identifiants des relations
        return [row["relId"] for row in results]


    # -------------------- MARQUAGE D'UN VOTE VALIDE --------------------

    @staticmethod
    def mark_vote_valid(rel_id: str):
        """
        Marque une relation VOTED comme validée :
        processed = true et valid = true.
        """
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(
                VoteRepository._mark_vote_valid_tx, rel_id
            )

    @staticmethod
    def _mark_vote_valid_tx(tx, rel_id: str):
        # Met à jour les propriétés processed et valid sur les relations
        tx.run(
            """
            MATCH (:User)-[v:VOTED]->(:User)
            WHERE elementId(v) = $id
            SET v.processed = true,
                v.valid = true,
                v.current = true
            """,
            id=rel_id,
        )


    # -------------------- MARQUAGE DES VOTES INVALIDES --------------------

    @staticmethod
    def mark_votes_invalid(rel_ids: list[str]):
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
    def _mark_votes_invalid_tx(tx, rel_ids: list[str]):
        # Même logique que mark_votes_valid, mais valid = false
        tx.run(
            """
            MATCH (:User)-[v:VOTED]->(:User)
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
            MATCH (voter:User)-[v:VOTED {processed: false}]->(:User)
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

        # Désactive le dernier vote actif si un nouveau arrive
        tx.run(
            """
            MATCH (voter:User)-[v:VOTED {processed: false}]->(target:User)
            WITH voter, v.domain AS vDomain, target
            MATCH (voter)-[v2:VOTED {current: true, domain: vDomain}]->(target)
            SET v2.current = false
            """
        )
        

        # Valide toutes les self-loop non traitées (processed=false)
        # Celles-ci sont marquées processed=true et valid=true
        tx.run(
            """
            MATCH (u:User)-[v:VOTED {processed: false}]->(u)
            SET v.processed = true, v.valid = true, v.current = true
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
    def _setup_recalculation_by_domain_tx(tx) -> list[str]:
        # 1. Remise à zéro des propriétés `count` et `cycle` de toutes les relations VOTED
        tx.run("""
            MATCH (:User)-[r:VOTED]->(:User)
            WHERE r.current = true
            SET r.count = null, r.cycle = false
        """)

        # 2. Collecte de tous les domaines présents dans les relations VOTED
        result = tx.run("MATCH ()-[r:VOTED]->() WHERE r.current = true RETURN DISTINCT r.domain AS domain")
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
    def _recalculate_counts_by_domain_tx(tx, domain: str):
        graph_name = f"myGraph_{domain}"

        # 4. Projection d'un sous-graphe GDS filtré par domaine
        #    On ne projette que les relations VOTED de ce domaine
        tx.run(
            """
            MATCH (u1:User)-[r:VOTED]->(u2:User)
            WHERE r.domain = $domain
            AND r.current = true
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
            AND r.current = true
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
            business_id = rec["businessId"]
            incoming_rec = tx.run(
                """
                MATCH (src:User)-[inR:VOTED]->(u:User)
                WHERE u.id = $businessId
                AND inR.cycle = false
                AND inR.domain = $domain
                AND inR.current = true
                RETURN sum(coalesce(inR.count, 0)) AS incoming
                """,
                businessId=business_id,
                domain=domain
            ).single()
            incoming = incoming_rec["incoming"] or 0

            tx.run(
                """
                MATCH (u:User)-[outR:VOTED]->(v:User)
                WHERE u.id = $businessId
                AND outR.cycle = false
                AND outR.domain = $domain
                AND outR.current = true
                SET outR.count = $newCount
                """,
                businessId=business_id,
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
                AND r.current = true
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
                AND r.current = true
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
                AND rel.current = true
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
    

    # -------------------- VERIFICATION DE LA VALIDITE D'UN VOTE --------------------
    
    @staticmethod
    def check_vote_validity(rel_id: str) -> tuple[int, list[str], bool]:
        """
        Vérifie si un vote (relation VOTED) est valide selon la logique de seuil et de cycle.

        :param rel_id: elementId() de la relation VOTED à vérifier
        :return: un tuple (count, relIds, cycle) :
                - count : le poids à attribuer si le vote est valide, ou -1 si invalidé  
                - relIds : la liste des elementId() des relations sur le chemin concerné  
                - cycle : booléen indiquant si le vote forme un cycle
        """
        driver = get_driver()
        with driver.session() as session:
            return session.execute_write(VoteRepository._check_vote_validity, rel_id)
        

    @staticmethod
    def _check_vote_validity(tx, rel_id: str) -> tuple[int, list[str], bool]:
        # Récupère le votant, la cible, et le domaine de la relation à valider
        rec = tx.run(
            """
            MATCH (u:User)-[v:VOTED]->(t:User)
            WHERE elementId(v) = $relId
            RETURN elementId(u) AS voterId, v.domain AS domain, t as target
            """,
            relId=rel_id
        ).single()
        voter_id = rec["voterId"]
        target = rec["target"]
        domain = rec["domain"]

        # Si la relation est un auto-vote (u == t), on marque comme cycle
        if voter_id == target.element_id:
            return 0, [], True

        # Recherche du chemin des votes valides à partir de la cible
        path = tx.run(
            """
            MATCH p = ((start:User)-[:VOTED* {domain: $domain, current: true}]->(n:User)
            WHERE elementId(start) = $startId)
            WITH nodes(p) AS allNodes, relationships(p) AS allRels
            ORDER BY length(p) DESC
            LIMIT 1
            RETURN allNodes, allRels
            """,
            startId=target.element_id,
            domain=domain
        ).single()
        nodes = path["allNodes"] or [] if path else []
        rels = path["allRels"] or [] if path else []

        # Si le dernier rel est une self-loop, on l’enlève
        if len(rels) and rels[-1].nodes[0].element_id == rels[-1].nodes[1].element_id:
            rels.pop()
            nodes.pop()
        elif not len(nodes):
            # S’il n’y a pas de chemin, on considère juste la cible
            nodes = [target]

        # Calcul des counts entrantes jusqu’au votant
        incoming_rec = tx.run(
            """
            MATCH (:User)-[inR:VOTED]->(u:User)
            WHERE elementId(u) = $endId
            AND inR.cycle = false
            AND inR.domain = $domain
            AND inR.current = true
            RETURN sum(coalesce(inR.count, 0)) AS incoming
            """,
            endId=voter_id,
            domain=domain
        ).single()
        incoming = incoming_rec["incoming"] or 0
        
        violated = False
        cycle = nodes[-1].element_id == voter_id

        if cycle:
            # Si c’est un cycle, vérifier seuils de tous les nœuds du cycle
            for node in nodes:
                threshold = node["threshold"]
                if threshold != -1 and incoming >= threshold:
                    violated = True
                    break

        else:
            # Chemin “normal” sans cycle
            for rel in rels:
                threshold = rel.nodes[0]["threshold"]
                incoming_sum = rel["count"] + incoming
                if rel["cycle"]:
                    incoming_sum += 1
                if threshold != -1 and incoming_sum > threshold:
                    violated = True
                    break

            if not violated:
                # Vérification supplémentaire avec le dernier nœud
                last_node_threshold = nodes[-1]["threshold"]
                if not(last_node_threshold == -1 or (len(rels) and rels[-1]["cycle"])):
                    last_node_incoming_rec = tx.run(
                        """
                        MATCH (:User)-[inR:VOTED]->(u:User)
                        WHERE elementId(u) = $endId
                        AND inR.cycle = false
                        AND inR.domain = $domain
                        AND inR.current = true
                        RETURN sum(coalesce(inR.count, 0)) AS incoming
                        """,
                        endId=nodes[-1].element_id,
                        domain=domain
                    ).single()
                    last_node_incoming = last_node_incoming_rec["incoming"] or 0
                    if last_node_incoming + incoming > nodes[-1]["threshold"]:
                        violated = True

        if violated:
            return -1, None, cycle
        
        # Si tout est OK, on renvoie le count, les relations du chemin, et si on crée un cycle
        return incoming + 1, [rel.element_id for rel in rels], cycle
    

    # -------------------- MISE A JOUR DES COUNTS D'UN NOUVEAU VOTE VALIDE --------------------

    @staticmethod
    def update_counts(rel_id: str, count: int, rel_ids: list[str], cycle: bool):
        """
        Met à jour les propriétés `count` et `cycle` d’un vote donné,
        et, si cycle, met à jour les votes sur tout le chemin.
        
        :param relId: elementId() de la relation à mettre à jour  
        :param count: nouveau poids à appliquer  
        :param relIds: liste d’elementId() des relations sur le chemin  
        :param cycle: booléen indiquant si c’est un cycle
        """
        driver = get_driver()
        with driver.session() as session:
            session.execute_write(VoteRepository._update_counts, rel_id, count, rel_ids, cycle)

    @staticmethod
    def _update_counts(tx, rel_id: str, count: int, rel_ids: list[str], cycle: bool):
        tx.run(
            """
            MATCH (:User)-[v:VOTED]->(:User)
            WHERE elementId(v) = $relId
            SET v.count = $count, v.cycle = $cycle
            """,
            relId=rel_id,
            count=count,
            cycle=cycle
        )

        if cycle:
            # Si c’est un cycle, on met le même count a toutes les relations du chemin
            tx.run(
                """
                MATCH (:User)-[v:VOTED]->(:User)
                WHERE elementId(v) IN $relIds
                SET v.count = $count, v.cycle = true
                """,
                relIds=rel_ids,
                count=count
            )
        
        else:
            # Sinon, on incrémente le count des relations du chemin
            tx.run(
                """
                MATCH (:User)-[v:VOTED]->(:User)
                WHERE elementId(v) IN $relIds
                SET v.count = v.count + $count
                """,
                relIds=rel_ids,
                count=count
            )

    def get_daily_votes_to_user(user_id: uuid4) -> List:
        drv = get_driver()
        with drv.session() as session:
            return session.execute_read(VoteRepository._get_daily_votes_to_user_tx, user_id)

    @staticmethod
    def _get_daily_votes_to_user_tx(tx, user_id: str) -> List:
        res = tx.run(
            """
            MATCH (:User)-[vote:VOTED]->(dst:User {id: $dst_id})
            RETURN date(vote.created_at) AS date, sum(vote.count) AS count
            ORDER BY date DESC
            """,
            dst_id=user_id
        )
        return list(res)

    @staticmethod
    def get_monthly_votes_to_user(user_id: uuid4) -> List:
        drv = get_driver()
        with drv.session() as session:
            return session.execute_read(VoteRepository._get_monthly_votes_to_user_tx, user_id)

    def _get_monthly_votes_to_user_tx(tx, user_id: str) -> List:
        res = tx.run(
            """
            MATCH (:User)-[vote:VOTED]->(dst:User {id: '4'})
            RETURN date(vote.created_at).year as year, date(vote.created_at).month AS month, sum(vote.count) AS count
            ORDER BY year, month desc
            """,
            dst_id=user_id
        )
        return list(res)

    @staticmethod
    def get_chart_for_domain(domain: str) -> List:
        drv = get_driver()
        with drv.session() as session:
            return session.execute_read(VoteRepository._get_chart_for_domain_tx, domain)

    def _get_chart_for_domain_tx(tx, domain: str) -> List:
        res = tx.run(
            """
            MATCH (:User {domain: $domain})-[v:VOTED]->(u:User {domain: $domain})
            WHERE NOT EXISTS ((u)-[:VOTED]->())
            AND v.created_at >= datetime() - duration({days:30})
            WITH u.id AS userId, date(v.created_at) AS day, sum(v.count) AS votes_per_day
            ORDER BY day desc
            WITH userId, collect({date: day, count: votes_per_day}) AS votes
            RETURN userId, votes
            """,
            domain=domain
        )

        returned = []
        for user_chart in res:
            votes = []
            for v in user_chart['votes']:
                votes.append({
                    'date': str(v['date']),
                    'count': v['count']
                })
            returned.append({
                'userId': user_chart['userId'],
                'votes': votes
            })
        return returned

    @staticmethod
    def get_all_domains() -> List:
        drv = get_driver()
        with drv.session() as session:
            return session.execute_read(VoteRepository._get_all_domains_tx)

    @staticmethod
    def _get_all_domains_tx(tx) -> List:
        res = tx.run(
            """
            MATCH (u:User)
            WHERE u.domain IS NOT NULL
            RETURN DISTINCT u.domain AS domain
            """
        )
        return [rec['domain'] for rec in res]

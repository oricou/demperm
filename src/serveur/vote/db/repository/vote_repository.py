from app.neo4j_config import get_driver


class VoteRepository:
    """
    Persistance des votes dans Neo4j.

    Modèle :
      (voter:User {id})
          -[:VOTED {id, createdAt, domain, count}]->
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

            OPTIONAL MATCH (voter)<-[incoming:VOTED {domain: $domain}]-()
            WITH voter, target,
                 coalesce(sum(incoming.count), 0) AS incomingSum

            WITH voter, target,
                 incomingSum + 1 AS voteWeight

            MERGE (voter)-[rel:VOTED {domain: $domain}]->(target)
            ON CREATE SET
                rel.id        = $id,
                rel.createdAt = datetime($createdAt),
                rel.count     = voteWeight
            ON MATCH SET
                rel.count     = rel.count + voteWeight
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
        result = tx.run(
            """
            MATCH (voter:User {id: $voterId})-[rel:VOTED {domain: $domain}]->(target:User)
            WITH rel
            DELETE rel
            RETURN count(rel) AS deletedCount
            """,
            voterId=str(voter_id),
            domain=domain,
        ).single()

        deleted_count = result["deletedCount"] if result is not None else 0
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
                MATCH (voter:User)-[rel:VOTED]->(target:User {id: $userId})
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

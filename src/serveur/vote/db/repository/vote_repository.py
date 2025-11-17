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

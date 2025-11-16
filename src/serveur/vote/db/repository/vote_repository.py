from app.neo4j_config import get_driver

class VoteRepository:
    """
    Persistance des votes dans Neo4j.

    Modèle simple :
      (voter:User {id})
          -[:VOTED {id, createdAt, domain}]->
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

            CREATE (voter)-[:VOTED {
                id: $id,
                domain: $domain,
                createdAt: datetime($createdAt)
            }]->(target)
            """,
            id=str(vote["id"]),
            voterId=str(vote["voterId"]),
            targetUserId=str(vote["targetUserId"]),
            domain=vote["domain"],
            createdAt=vote["createdAt"].isoformat(),
        )

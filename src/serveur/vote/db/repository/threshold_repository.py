from app.neo4j_config import get_driver


class ThresholdRepository:
    """
    persistance des seuils de publication dans Neo4j.
    
    Modèle :
      (user:User {id, threshold})
      
    Valeur par défaut : 100
    """

    @staticmethod
    def get_threshold_setting(user_id: str) -> dict:
        """
        Returns:
            dict avec userId et threshold
            Si l'utilisateur n'existe pas, retourne threshold=100 par défaut
        """
        driver = get_driver()
        with driver.session() as session:
            result = session.execute_read(
                ThresholdRepository._get_threshold_setting_tx,
                user_id
            )
            return result

    @staticmethod
    def _get_threshold_setting_tx(tx, user_id: str) -> dict:
        result = tx.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.id AS userId, 
                   COALESCE(u.threshold, 100) AS threshold
            """,
            userId=user_id
        )
        record = result.single()
        
        if record:
            return {
                "userId": record["userId"],
                "threshold": record["threshold"]
            }
        
        return {
            "userId": user_id,
            "threshold": 100
        }

    @staticmethod
    def update_threshold_setting(user_id: str, threshold: int) -> dict:
        """ 
        Returns:
            dict avec userId et threshold mis à jour
        """
        driver = get_driver()
        with driver.session() as session:
            result = session.execute_write(
                ThresholdRepository._update_threshold_setting_tx,
                user_id,
                threshold
            )
            return result

    @staticmethod
    def _update_threshold_setting_tx(tx, user_id: str, threshold: int) -> dict:
        result = tx.run(
            """
            MERGE (u:User {id: $userId})
            SET u.threshold = $threshold
            RETURN u.id AS userId, u.threshold AS threshold
            """,
            userId=user_id,
            threshold=threshold
        )
        record = result.single()
        
        return {
            "userId": record["userId"],
            "threshold": record["threshold"]
        }

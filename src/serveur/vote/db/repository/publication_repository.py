from app.neo4j_config import get_driver


class PublicationRepository:
    """
    Gestion de la persistance des préférences de publication dans Neo4j.
    
    Modèle :
      (user:User {id, publishVotes})
      
    La propriété publishVotes indique si l'utilisateur accepte
    la publication automatique de son nombre de voix.
    Valeur par défaut : True (publication acceptée)
    """

    @staticmethod
    def get_publication_setting(user_id: str) -> dict:
        """
        Récupère les paramètres de publication d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            dict avec userId et publishVotes
            Si l'utilisateur n'existe pas, retourne publishVotes=True et threshold=-1 par défaut
        """
        driver = get_driver()
        with driver.session() as session:
            result = session.execute_read(
                PublicationRepository._get_publication_setting_tx,
                user_id
            )
            return result

    @staticmethod
    def _get_publication_setting_tx(tx, user_id: str) -> dict:
        """
        Transaction de lecture pour récupérer le paramètre publishVotes.
        """
        result = tx.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.id AS userId, 
                   COALESCE(u.publishVotes, true) AS publishVotes,
                   COALESCE(u.threshold, -1) AS threshold
            """,
            userId=user_id
        )
        record = result.single()
        
        if record:
            return {
                "publishVotes": record["publishVotes"],
                "threshold": record["threshold"]
            }
        
        # Si l'utilisateur n'existe pas encore, retourner la valeur par défaut
        return {
            "publishVotes": True,
            "threshold": -1
        }

    @staticmethod
    def update_publication_setting(user_id: str, publish_votes: bool, threshold: int) -> dict:
        """
        Met à jour le paramètre de publication d'un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            publish_votes: Nouvelle valeur du paramètre
            threshold: Nouvelle valeur du paramètre
            
        Returns:
            dict avec publishVotes et threshold mis à jour
        """
        driver = get_driver()
        with driver.session() as session:
            result = session.execute_write(
                PublicationRepository._update_publication_setting_tx,
                user_id,
                publish_votes,
                threshold
            )
            return result

    @staticmethod
    def _update_publication_setting_tx(tx, user_id: str, publish_votes: bool, threshold: int) -> dict:
        """
        Transaction d'écriture pour mettre à jour publishVotes.
        """
        result = tx.run(
            """
            MERGE (u:User {id: $userId})
            SET u.publishVotes = $publishVotes,
                u.threshold = $threshold
            RETURN u.publishVotes AS publishVotes, u.threshold AS threshold
            """,
            userId=user_id,
            publishVotes=publish_votes,
            threshold=threshold
        )
        record = result.single()
        
        return {
            "publishVotes": record["publishVotes"],
            "threshold": record["threshold"]
        }

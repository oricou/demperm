from db.repository.publication_repository import PublicationRepository


class PublicationService:
    @staticmethod
    def get_publication_setting(user_id: str) -> dict:
        """
        Récupère les paramètres de publication d'un utilisateur. return dict contenant userId et publishVotes
        """
        return PublicationRepository.get_publication_setting(user_id)

    @staticmethod
    def update_publication_setting(user_id: str, publish_votes: bool) -> dict:
        """
        Met à jour le paramètre de publication d'un utilisateur. return dict contenant userId et publishVotes mis à jour
        """
        return PublicationRepository.update_publication_setting(user_id, publish_votes)

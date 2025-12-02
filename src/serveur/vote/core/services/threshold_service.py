from db.repository.threshold_repository import ThresholdRepository


class ThresholdService:
    @staticmethod
    def get_threshold_setting(user_id: str) -> dict:
        """
        Récupère le seuil de publication d'un utilisateur. Returns dict contenant userId et threshold
        """
        return ThresholdRepository.get_threshold_setting(user_id)

    @staticmethod
    def update_threshold_setting(user_id: str, threshold: int) -> dict:
        """
        Met à jour le seuil de publication d'un utilisateur. Returns dict contenant userId et threshold mis à jour
        """
        return ThresholdRepository.update_threshold_setting(user_id, threshold)

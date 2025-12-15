import os
from typing import List
from db.repository.vote_repository import VoteRepository

MIN_PUBLIC_VOTES = int(os.getenv("MIN_PUBLIC_VOTES", 5))

class StatsService:
    @staticmethod
    def get_daily_stats(user_id: str, days: int = 30, include_monthly: bool = False) -> dict:
        """
        Retourne:
        {
          'userId': str,
          'byDomain': [ {domain: str, series: [{date, count}, ...]}, ... ],
          'monthlyByDomain': [ {domain: str, series: [{year,month,count}, ...]}, ... ]  # si include_monthly True
        }
        """
        by_domain, publish_votes = VoteRepository.get_daily_votes_to_user(user_id, days)
        last_update = VoteRepository.get_last_update()
        if not publish_votes:
            filtered_domains = []

            for domain_entry in by_domain:
                series = domain_entry.get("series", [])
                if not series:
                    continue

                first = series[0]
                first_date = first.get("date")
                first_count = first.get("count", 0)

                if (
                    first_date == last_update
                    and first_count >= MIN_PUBLIC_VOTES
                ):
                    filtered_domains.append(domain_entry)

            by_domain = filtered_domains

        res = {"userId": user_id, "byDomain": by_domain}

        if include_monthly:
            monthly_by_domain = VoteRepository.get_monthly_votes_to_user(user_id)
            res["monthlyByDomain"] = monthly_by_domain
        return res

    @staticmethod
    def get_monthly_stats(user_id: str, months: int = 12) -> List:
        """
        Retourne une liste: [ {domain: str, series: [{year,month,count}, ...]}, ... ]
        """
        return VoteRepository.get_monthly_votes_to_user(user_id, months)
        
    @staticmethod
    def get_chart(domain: str | None = None, days: int = 30) -> List:
        """
        Retourne pour chaque domaine (ou pour un domaine donné) la liste des top users.
        Si domain est None, on génère pour tous les domaines trouvés.
        """
        domains = VoteRepository.get_all_domains()
        res = []
        if domain:
            domains = [domain] if domain in domains else []

        for d in domains:
            users = VoteRepository.get_chart_for_domain(d, days)
            res.append({"domain": d, "users": users})
        return res

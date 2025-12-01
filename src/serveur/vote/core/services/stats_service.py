from db.repository.vote_repository import VoteRepository

from typing import List

class StatsService:
    @staticmethod
    def get_daily_stats(user_id: str) -> List:
        """
        """
        return VoteRepository.get_daily_votes_to_user(user_id)

    @staticmethod
    def get_monthly_stats(user_id: str) -> dict:
        """
        """
        return VoteRepository.get_monthly_votes_to_user(user_id)

    @staticmethod
    def get_chart() -> dict:
        """
        """
        domains = VoteRepository.get_all_domains()

        res = []
        print(domains)
        for d in domains:
            sub_chart = VoteRepository.get_chart_for_domain(d)
            res.append({'domain': d, 'users': sub_chart})
        return res

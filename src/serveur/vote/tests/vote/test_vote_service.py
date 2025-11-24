import uuid
from datetime import datetime
from django.utils import timezone

from core.services.vote_service import VoteService


class DummyVoteRepository:
    called_with = None

    @staticmethod
    def save_vote(vote: dict) -> None:
        DummyVoteRepository.called_with = vote


def test_create_vote_builds_correct_structure(monkeypatch):
    monkeypatch.setattr(
        "core.services.vote_service.VoteRepository",
        DummyVoteRepository,
        raising=True,
    )

    voter_id = "11111111-1111-1111-1111-111111111111"
    target_user_id = "22222222-2222-2222-2222-222222222222"
    domain = "tech"

    vote = VoteService.create_vote(
        voter_id=voter_id,
        target_user_id=target_user_id,
        domain=domain,
    )

    assert isinstance(vote["id"], uuid.UUID)
    assert vote["voterId"] == voter_id
    assert vote["targetUserId"] == target_user_id
    assert vote["domain"] == domain
    assert isinstance(vote["createdAt"], datetime)

    now = timezone.now()
    assert abs((now - vote["createdAt"]).total_seconds()) < 10

    assert DummyVoteRepository.called_with is vote

def test_delete_vote_delegates_to_repository(monkeypatch):
    class DummyRepo:
        called_with = None
        return_value = True

        @staticmethod
        def delete_vote_for_voter_and_domain(voter_id: str, domain: str) -> bool:
            DummyRepo.called_with = (voter_id, domain)
            return DummyRepo.return_value

    monkeypatch.setattr(
        "core.services.vote_service.VoteRepository",
        DummyRepo,
        raising=True,
    )

    voter_id = "11111111-1111-1111-1111-111111111111"
    domain = "tech"

    DummyRepo.return_value = True
    result = VoteService.delete_vote(voter_id=voter_id, domain=domain)

    assert result is True
    assert DummyRepo.called_with == (voter_id, domain)

    DummyRepo.return_value = False
    result = VoteService.delete_vote(voter_id=voter_id, domain=domain)

    assert result is False
    assert DummyRepo.called_with == (voter_id, domain)


def test_get_votes_by_voter_delegates_to_repository(monkeypatch):
    class DummyRepo:
        called_with = None
        return_value = [
            {"id": "vote-1", "voterId": "v1", "targetUserId": "t1", "domain": "tech", "createdAt": timezone.now()},
            {"id": "vote-2", "voterId": "v1", "targetUserId": "t2", "domain": "design", "createdAt": timezone.now()},
        ]

        @staticmethod
        def find_votes_by_voter(voter_id: str, domain: str | None = None):
            DummyRepo.called_with = (voter_id, domain)
            return DummyRepo.return_value

    monkeypatch.setattr(
        "core.services.vote_service.VoteRepository",
        DummyRepo,
        raising=True,
    )

    voter_id = "11111111-1111-1111-1111-111111111111"

    votes = VoteService.get_votes_by_voter(voter_id=voter_id, domain=None)

    assert votes is DummyRepo.return_value
    assert DummyRepo.called_with == (voter_id, None)

    votes = VoteService.get_votes_by_voter(voter_id=voter_id, domain="tech")

    assert votes is DummyRepo.return_value
    assert DummyRepo.called_with == (voter_id, "tech")


def test_get_received_votes_delegates_to_repository(monkeypatch):
    class DummyRepo:
        called_with = None
        return_value = {
            "userId": "22222222-2222-2222-2222-222222222222",
            "total": 3,
            "byDomain": {"tech": 2, "design": 1},
            "usersByDomain": {
                "tech": [
                    "11111111-1111-1111-1111-111111111111",
                    "33333333-3333-3333-3333-333333333333",
                ],
                "design": [
                    "44444444-4444-4444-4444-444444444444",
                ],
            },
        }

        @staticmethod
        def get_received_votes_summary(user_id: str, domain: str | None = None) -> dict:
            DummyRepo.called_with = (user_id, domain)
            return DummyRepo.return_value

    monkeypatch.setattr(
        "core.services.vote_service.VoteRepository",
        DummyRepo,
        raising=True,
    )

    user_id = "22222222-2222-2222-2222-222222222222"

    summary = VoteService.get_received_votes(user_id=user_id, domain=None)

    assert summary is DummyRepo.return_value
    assert DummyRepo.called_with == (user_id, None)

    summary = VoteService.get_received_votes(user_id=user_id, domain="tech")

    assert summary is DummyRepo.return_value
    assert DummyRepo.called_with == (user_id, "tech")


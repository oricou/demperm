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

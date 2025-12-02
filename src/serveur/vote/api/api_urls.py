# api_urls.py
from django.urls import path
from api.vote_controller import (
    VoteDeleteView,
    VoteValidationView,
    VoteView,
    VotesByVoterView,
    VotesByVoterMeView,
    VotesForUserView,
    VotesForUserMeView,
)
from api.publication_controller import PublicationSettingView
from api.result_controller import ResultView

urlpatterns = [
    path("votes", VoteView.as_view(), name="create_vote"),
    path("votes/<str:domain>", VoteDeleteView.as_view(), name="delete_vote"),

    path("votes/by-voter/me", VotesByVoterMeView.as_view(), name="votes_by_voter_me"),
    path("votes/by-voter/<str:voterId>", VotesByVoterView.as_view(), name="votes_by_voter"),
    path("votes/for-user/me", VotesForUserMeView.as_view(), name="votes_for_user_me"),
    path("votes/for-user/<str:userId>", VotesForUserView.as_view(), name="votes_for_user"),

    path("votes/validate/force", VoteValidationView.as_view(), name="vote_validation"),
    
    path("results", ResultView.as_view(), name="get_results"),

    path("publication", PublicationSettingView.as_view(), name="publication_setting"),
]

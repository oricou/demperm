from core.services.vote_validation_service import VoteValidationService

def process_daily_votes():
    VoteValidationService.process_daily_votes()
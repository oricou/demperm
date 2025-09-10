from django.shortcuts import render
from django.http import HttpResponse
from .models import Proposal, Poll


def index(request):
    """Homepage view"""
    return HttpResponse("Welcome to Demperm - Democratic Participation Platform")


def proposals(request):
    """List all proposals"""
    proposals = Proposal.objects.all()
    return HttpResponse(f"Found {proposals.count()} proposals in the database")


def polls(request):
    """List all polls"""
    polls = Poll.objects.all()
    return HttpResponse(f"Found {polls.count()} polls in the database")

"""
URL configuration for domains app.
"""
from django.urls import path
from .views import (
    DomainsListView, DomainDetailView, DomainSubforumsView, CreateDomainSubforumView
)

app_name = 'domains'

urlpatterns = [
    # Domains
    path('', DomainsListView.as_view(), name='domains-list'),
    path('<str:domain_id>/', DomainDetailView.as_view(), name='domain-detail'),
    path('<str:domain_id>/subforums/', DomainSubforumsView.as_view(), name='domain-subforums'),
    path('<str:domain_id>/subforums/create/', CreateDomainSubforumView.as_view(), name='create-subforum'),
]


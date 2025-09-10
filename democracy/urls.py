from django.urls import path
from . import views

app_name = 'democracy'

urlpatterns = [
    # Basic URLs for future development
    path('', views.index, name='index'),
    path('proposals/', views.proposals, name='proposals'),
    path('polls/', views.polls, name='polls'),
]
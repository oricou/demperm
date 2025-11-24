"""
URL configuration for vote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from api.vote_controller import VoteView
from api.publication_controller import PublicationSettingView
from api.threshold_controller import ThresholdSettingView

urlpatterns = [
    path("votes", VoteView.as_view(), name="create_vote"),
    path("publication/<str:userId>", PublicationSettingView.as_view(), name="publication_setting"),
    path("threshold/<str:userId>", ThresholdSettingView.as_view(), name="threshold_setting"),
]

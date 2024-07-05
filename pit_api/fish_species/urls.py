from django.urls import path

from pit_api.fish_species.views import FishSpeciesAPIView

urlpatterns = [
    path("", FishSpeciesAPIView.as_view()),
]

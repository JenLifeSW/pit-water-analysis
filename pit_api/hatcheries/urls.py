from django.urls import path

from pit_api.hatcheries.views import HatcheryAPIView, HatcheryInfoAPIView, AddTankAPIView

urlpatterns = [
    path("", HatcheryAPIView.as_view()),
    path("/<int:hatchery_id>", HatcheryInfoAPIView.as_view()),
    path("/<int:hatchery_id>/tanks", AddTankAPIView.as_view()),
]

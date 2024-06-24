from django.urls import path

from pit_api.measurements.views import MeasurementHistoryAPIView
from pit_api.tanks.views import TankInfoAPIView

urlpatterns = [
    path("/<int:tank_id>", TankInfoAPIView.as_view()),
    path("/<int:tank_id>/measured-datas", MeasurementHistoryAPIView.as_view()),
]

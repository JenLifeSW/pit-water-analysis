from django.urls import path

from pit_api.users.views import UserInfoAPIView

urlpatterns = [
    path("/info", UserInfoAPIView.as_view()),
]

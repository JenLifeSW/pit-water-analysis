from django.urls import path

from pit_api.auth.views import RegistrationAPIView, LoginAPIView, SendVerificationEmail, RefreshTokenAPIView, \
    VerifyEmail

urlpatterns = [
    # path("/registration", RegistrationAPIView.as_view()),
    path("/login", LoginAPIView.as_view()),
    path("/refresh", RefreshTokenAPIView.as_view()),
    # path("/send-verification-email", SendVerificationEmail.as_view()),
    # path("/verify-email", VerifyEmail.as_view()),
]

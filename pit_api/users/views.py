from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from pit_api.auth.models import Role
from pit_api.common.views import BaseAPIView


class UserInfoAPIView(BaseAPIView):
    def get(self, request):
        user = JWTAuthentication().authenticate(request)[0]
        role = Role.objects.filter(id=user.role.id)
        user_data = {
            "nickname": user.nickname
        }

    def post(self, request):
        nickname = request.data.get("nickname")
        email = request.data.get("email")
        verification_token = request.data.get("verificationToken")
        phone = request.data.get("phone")

        return Response(status=status.HTTP_200_OK)

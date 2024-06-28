from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from pit_api.users.models import User


class BaseAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testUser"
        cls.password = "password"
        cls.nickname = "nickname"
        cls.role_id = 0

        cls.user = User.objects.create(
            username=cls.username,
            password=make_password(cls.password),
            nickname=cls.nickname,
            role_id=cls.role_id,
            created_at=timezone.now()
        )
        cls.refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(cls.refresh.access_token)


class AuthenticatedUserAPITestCase(BaseAPITestCase):
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def change_role_id(self, role_id):
        self.user.role_id = role_id
        self.user.save()
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(RefreshToken.for_user(self.user).access_token)


class AuthenticatedManagerAPITestCase(AuthenticatedUserAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        super().change_role_id(cls, 10)


class AuthenticatedAdminAPITestCase(AuthenticatedUserAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        super().change_role_id(cls, 20)


class AuthenticatedOperatorAPITestCase(AuthenticatedUserAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        super().change_role_id(cls, 30)

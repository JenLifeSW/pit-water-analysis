from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from pit_api.fish_species.models import FishSpecies
from pit_api.hatcheries.models import Hatchery, HatcheryManagerAssociation
from pit_api.tanks.models import Tank
from pit_api.tests import AuthenticatedAdminAPITestCase, AuthenticatedManagerAPITestCase
from pit_api.users.models import User


# 양식장 추가
class TestAPIAddHatchery(AuthenticatedAdminAPITestCase):
    name = "테스트 양식장 1a"
    url = "/api/hatcheries"

    def test_success(self):
        data = {"name": self.name}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("hatcheries", response.data)

    def test_no_response_body(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 이름을 입력하세요.")

    def test_duplicate_name(self):
        hatchery = Hatchery.objects.create(name=self.name, created_at=timezone.now())
        HatcheryManagerAssociation.objects.create(user=self.user, hatchery=hatchery)

        data = {"name": self.name}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "이미 사용중인 양식장 이름입니다.")

    def test_wrong_name1_min_length(self):
        data = {"name": "1"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 이름의 길이는 2자 이상이어야 합니다.")

    def test_wrong_name2_max_length(self):
        data = {"name": '1' * 17}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 이름의 길이는 16자를 초과할 수 없습니다.")

    def test_wrong_name3_special_character(self):
        data = {"name": f"{self.name} !"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 이름에 특수문자를 사용할 수 없습니다.")

    def test_wrong_description1_max_length(self):
        data = {"name": self.name, "description": "a" * 256}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 설명의 길이는 255자를 초과할 수 없습니다.")

    def test_wrong_description2_special_character(self):
        data = {"name": self.name, "description": "&"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 설명에 사용할 수 없는 기호가 포함되어 있습니다.")

    def test_wrong_address1_max_length(self):
        data = {"name": self.name, "address": "a" * 101}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 주소의 길이는 100자를 초과할 수 없습니다.")

    def test_wrong_address2_special_character(self):
        data = {"name": self.name, "address": "&"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "양식장 주소에 사용할 수 없는 기호가 포함되어 있습니다.")


# 어드민 미만 권한 양식장 추가시 실패
class TestAPIAddHatcheryWithUnderAdminAuth(AuthenticatedManagerAPITestCase):
    name = "테스트 양식장 1a"
    url = "/api/hatcheries"

    def test_fail(self):
        data = {"name": self.name}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# 양식장 리스트 조회
class TestAPIGetHatcheryList(AuthenticatedAdminAPITestCase):
    url = "/api/hatcheries"

    def test_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("hatcheries", response.data)


# 어드민 미만 권한 양식장 리스트 조회시 실패
class TestAPIGetHatcheryListWithUnderAdminAuth(AuthenticatedManagerAPITestCase):
    url = "/api/hatcheries"

    def test_fail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# 양식장 테스트 케이스 셋업 데이터
class _HatcheryInfoSetUppedTestCase(AuthenticatedAdminAPITestCase):
    name = "테스트 양식장 1a"
    tank_name = "수조 셋업"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.hatchery = Hatchery.objects.create(name=cls.name, created_at=timezone.now())
        HatcheryManagerAssociation.objects.create(user=cls.user, hatchery=cls.hatchery)
        cls.url = f"/api/hatcheries/{cls.hatchery.id}"

        cls.fish_species_id = 1
        cls.fish_species = FishSpecies.objects.get(id=cls.fish_species_id)
        cls.tank = Tank.objects.create(name=cls.tank_name, hatchery=cls.hatchery, fish_species=cls.fish_species)

    def set_forbidden_user(self):
        self.other_user = User.objects.create(
            username="other",
            password="other",
            nickname="other",
            role_id="20",
            created_at=timezone.now()
        )
        access_token = str(RefreshToken.for_user(self.other_user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


# 양식장 테스트 케이스 매니저 권한 유저 셋업 데이터
class _HatcheryInfoSetUppedTestCaseWithManagerAuth(_HatcheryInfoSetUppedTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        super().change_role_id(cls, 10)


# 양식장 수정
class TestAPIUpdateHatcheryInfo(_HatcheryInfoSetUppedTestCaseWithManagerAuth):
    def test_success(self):
        data = {"name": "양식장 이름 변경"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("hatchery", response.data)
        self.assertIn("tanks", response.data["hatchery"])
        self.assertIn("fishSpecies", response.data["hatchery"]["tanks"][0])

    def test_try_forbidden_user(self):
        self.set_forbidden_user()

        data = {"name": "양식장 이름 변경"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "이 양식장에 접근할 권한이 없습니다.")


# 양식장 정보 조회
class TestAPIGetHatcheryInfo(_HatcheryInfoSetUppedTestCaseWithManagerAuth):
    def test_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("hatchery", response.data)
        self.assertIn("tanks", response.data["hatchery"])
        self.assertIn("fishSpecies", response.data["hatchery"]["tanks"][0])

    def test_try_forbidden_user(self):
        self.set_forbidden_user()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "이 양식장에 접근할 권한이 없습니다.")


# 어드민 미만 권한 유저(매니저)가 양식장 삭제 시도시 실패
class TestAPIDeleteHatcheryWithUnderAdminAuth(_HatcheryInfoSetUppedTestCaseWithManagerAuth):
    def test_fail(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# 양식장 삭제는 어드민 권한 유저만 가능
class TestAPIDeleteHatchery(_HatcheryInfoSetUppedTestCase):
    def test_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_try_forbidden_user(self):
        self.set_forbidden_user()

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "이 양식장에 접근할 권한이 없습니다.")

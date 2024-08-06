import re

from rest_framework import status

from pit_api.hatcheries.tests import _HatcheryInfoSetUppedTestCaseWithManagerAuth
from pit_api.measurements.models import MeasurementTarget, MeasurementData, TankTargetAssociation


# 수조 테스트 케이스 셋업
class _AddTankSetUppedTestCase(_HatcheryInfoSetUppedTestCaseWithManagerAuth):
    name = "수조 추가 1a"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.target = MeasurementTarget.objects.create(name="질산성 질소", display_unit="ppm")
        tank_target_association = TankTargetAssociation.objects.create(tank=cls.tank, target=cls.target)
        cls.measurement_data = MeasurementData.objects.create(
            # tank=cls.tank,
            # target=cls.target,
            tank_target=tank_target_association,
            value=10,
            index=0
        )

    def setUp(self):
        super().setUp()
        self.url = self.url + "/tanks"


# 수조 상세 정보 테스트 셋업
class _TankInfoSetUppedTestCase(_AddTankSetUppedTestCase):
    def setUp(self):
        super().setUp()
        self.url = f"/api/tanks/{self.tank.id}"

    def assert_tank_info(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tank", response.data)
        self.assertIn("fishSpecies", response.data["tank"])
        self.assertIn("lastMeasurementDatas", response.data["tank"])
        self.assertIn("target", response.data["tank"]["lastMeasurementDatas"][0])


class TestAPIAddTank(_AddTankSetUppedTestCase):
    def test_success(self):
        data = {"name": self.name, "fishSpeciesId": self.fish_species_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tanks", response.data)
        self.assertIn("fishSpecies", response.data["tanks"][0])

    def test_wrong_hatchery_id(self):
        data = {"name": self.name, "fishSpeciesId": self.fish_species_id}
        url = re.sub(r'\d+', '0', self.url)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "양식장 정보를 찾을 수 없습니다.")

    def test_no_name(self):
        data = {"fishSpeciesId": self.fish_species_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "수조 이름을 입력하세요.")

    def test_no_fish_species_id(self):
        data = {"name": self.name}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "어종 정보를 찾을 수 없습니다.")

    def test_duplicate_name(self):
        data = {"name": self.tank_name, "fishSpeciesId": self.fish_species_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "이미 사용중인 수조 이름입니다.")

    def test_wrong_name1_min_length(self):
        data = {"name": "1", "fishSpeciesId": self.fish_species_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "수조 이름의 길이는 2자 이상이어야 합니다.")

    def test_wrong_name2_max_length(self):
        data = {"name": "1" * 17, "fishSpeciesId": self.fish_species_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "수조 이름의 길이는 16자를 초과할 수 없습니다.")

    def test_wrong_name3_special_character(self):
        data = {"name": f"{self.name} !", "fishSpeciesId": self.fish_species_id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "수조 이름에 특수문자를 사용할 수 없습니다.")

    def test_wrong_description1_max_length(self):
        data = {"name": self.name, "fishSpeciesId": self.fish_species_id, "description": "a" * 256}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "수조 설명의 길이는 255자를 초과할 수 없습니다.")


# 수조 수정
class TestAPIUpdateTankInfo(_TankInfoSetUppedTestCase):
    def test_success(self):
        data = {"name": "수조 이름 변경"}
        response = self.client.patch(self.url, data)
        self.assert_tank_info(response)

    def test_try_forbidden_user(self):
        self.set_forbidden_user()

        data = {"name": "수조 이름 변경"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "이 수조에 접근할 권한이 없습니다.")


# 수조 조회
class TestAPIGetTankInfo(_TankInfoSetUppedTestCase):
    def test_success(self):
        response = self.client.get(self.url)
        self.assert_tank_info(response)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn("tank", response.data)
        # self.assertIn("fishSpecies", response.data["tank"])
        # self.assertIn("measurementDatas", response.data["tank"])
        # self.assertIn("target", response.data["tank"]["measurementDatas"][0])

    def test_try_forbidden_user(self):
        self.set_forbidden_user()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "이 수조에 접근할 권한이 없습니다.")


# 수조 삭제
class TestAPIDeleteTankInfo(_TankInfoSetUppedTestCase):
    def test_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_try_forbidden_user(self):
        self.set_forbidden_user()

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "이 수조에 접근할 권한이 없습니다.")

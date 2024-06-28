from rest_framework import status

from pit_api.tanks.tests import _TankInfoSetUppedTestCase


class TestAPIGetMeasuredDatas(_TankInfoSetUppedTestCase):
    def setUp(self):
        super().setUp()
        self.url = self.url + "/measured-datas"

    def assert_success(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("target", response.data)
        self.assertIn("measurementDatas", response.data)
        self.assertIn("grades", response.data)

    def test_success_only_target_id_query(self):
        params = {"target-id": self.target.id}
        response = self.client.get(self.url, params)
        self.assert_success(response)

    def test_success_with_weeks(self):
        params = {"target-id": self.target.id, "weeks": 3}
        response = self.client.get(self.url, params)
        self.assert_success(response)

    def test_success_with_duration(self):
        params = {"target-id": self.target.id, "start-date": "2024-05-10", "end-date": "2024-06-10"}
        response = self.client.get(self.url, params)
        self.assert_success(response)

    def test_no_query_fail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(response.data["message"], "측정 항목 id를 입력하세요.")

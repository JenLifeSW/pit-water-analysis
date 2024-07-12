from rest_framework import status

from pit_api.tests import BaseAPITestCase


class TestAPIRegistration(BaseAPITestCase):
    url = "/api/auth/registration"
    new_username = "newUser"
    new_password = "password123"

    def test_success(self):
        data = {"username": self.new_username, "password": self.new_password, "nickname": "newUser"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_success_no_nickname(self):
        data = {"username": self.new_username, "password": self.new_password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_username(self):
        data = {"password": self.new_password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "아이디 또는 비밀번호가 입력되지 않았습니다.")

    def test_no_password(self):
        data = {"username": self.new_username}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "아이디 또는 비밀번호가 입력되지 않았습니다.")

    def test_duplicate_username(self):
        data = {"username": "testUser", "password": self.new_password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "이미 사용중인 아이디입니다.")

    def test_duplicate_nickname(self):
        data = {"username": self.new_username, "password": self.new_password, "nickname": "nickname"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "이미 사용중인 닉네임입니다.")

    def test_wrong_username1_special_character(self):
        data = {"username": "newUser!", "password": self.new_password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "아이디는 영문 대소문자와 숫자만 사용가능합니다.")

    def test_wrong_password1_no_english(self):
        data = {"username": self.new_username, "password": "12341234"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "비밀번호는 영문자를 포함해야 합니다.")

    def test_wrong_password2_no_digit(self):
        data = {"username": self.new_username, "password": "qwerqwer"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "비밀번호는 숫자를 포함해야 합니다.")

    def test_wrong_password3_special_character(self):
        data = {"username": self.new_username, "password": "wrong&1"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("특수문자", response.data["message"])

    def test_wrong_nickname1(self):
        data = {"username": self.new_username, "password": self.new_password, "nickname": "wrong!"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "닉네임은 한글 또는 영문, 숫자만 사용 가능합니다.")


class TestAPILogin(BaseAPITestCase):
    url = "/api/auth/login"

    def test_success(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Authorization", response.headers)
        self.assertTrue("Bearer " in response.headers["Authorization"])

    def test_wrong_password(self):
        data = {
            'username': self.username,
            'password': f"{self.password} wrong",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("Authorization", response.headers)
        self.assertEqual(response.data["message"], "아이디 또는 비밀번호를 확인하세요.")


class TestAPIRefresh(BaseAPITestCase):
    url = "/api/auth/refresh"

    def test_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh}")

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("Authorization", response.headers)
        self.assertTrue("Bearer " in response.headers["Authorization"])

    def test_try_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

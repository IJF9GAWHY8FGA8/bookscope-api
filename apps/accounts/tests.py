from rest_framework import status
from rest_framework.test import APITestCase


class AccountsAPITestCase(APITestCase):
    def test_register_and_get_current_user(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "reader1",
                "email": "reader1@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)

        access_token = response.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        me_response = self.client.get("/api/auth/me/")
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data["username"], "reader1")

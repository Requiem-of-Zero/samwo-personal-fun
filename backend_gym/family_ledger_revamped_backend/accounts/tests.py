from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
User = get_user_model()

class UserServiceAPITests(APITestCase):
    """
    TDD implementation for user auth
    """

    def setup(self):
        self.register_url = "/api/v1/auth/register/"
        self.login_url = "/api/v1/auth/login/"
        self.logout_url = "/api/v1/auth/logout/"
        self.me_url = "/api/v1/auth/me"
        self.change_password_url = "/api/v1/auth/change-password/"
        self.deactivate_url = "/api/v1/auth/deactivate"

        self.user_payload = {
            "email": "sam@example.com",
            "username": "sam",
            "password": "password123",
        }

    """
    Create user tests
    """
    def test_create_user_register_success(self):
        res = self.client.post(self.register_url, self.user_payload, format="json") # Simulates POST req to register endpoint

        self.assertEqual(res.status_code, status.HTTP_201_CREATED) # The response status code must equal 201 for created
        self.assertTrue( # Checks if the user exists in the db after registering the payload
            User.objects.filter(email="sam@example.com").exists()
        )

        user = User.objects.get(email=self.user_payload["email"]) # Fetch the user from the DB

        self.assertNotEqual(user.password, self.user_payload["password"]) # Stored user password does not equal the plaintext password from the mock payload

        self.assertTrue(user.check_password(self.user_payload["password"])) # Use built in auth check_password() from django to verify password stored is not in plaintext

        self.assertNotIn("password", res.data) # Verifys that the API response does not leak password data

    """
    Create duplicate email test
    """
    def test_create_user_register_duplicate_email_rejected(self):
        # Create a user in the DB
        User.objects.create_user(
            email="sam@example.com",
            username="other",
            password="password234"
        )

        res = self.client.post(
            self.register_url,
            self.user_payload,
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # Ensure the return code is a 400 bad request if a duplicate email entry is detected

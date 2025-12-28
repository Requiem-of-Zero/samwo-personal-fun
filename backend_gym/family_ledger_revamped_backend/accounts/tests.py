from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
User = get_user_model()

def create_user(email, username, password):
    return User.objects.create_user(email=email, username=username, password=password)

def login_and_get_tokens(client, email, password, login_url):
    """
    Logs in via /login/ and returns (access, refresh).
    """
    res = client.post(login_url, {
        "email": email,
        "password": password
    }, format="json")

    # access_token = res.data["access"], res.data["refresh"]
    # print(access_token)
    return res.data["access"], res.data["refresh"]

class UserServiceAPITests(APITestCase):

    """
    TDD implementation for user auth
    """
    def setUp(self):
        self.register_url = "/api/v1/auth/register/"
        self.login_url = "/api/v1/auth/login/"
        self.logout_url = "/api/v1/auth/logout/"
        self.me_url = "/api/v1/auth/me/"
        self.refresh_url = "/api/v1/auth/refresh/" 
        self.change_password_url = "/api/v1/auth/change-password/"
        self.deactivate_url = "/api/v1/auth/deactivate/"

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
        create_user("sam@example.com", "other", "password234")

        res = self.client.post(
            self.register_url,
            self.user_payload,
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # Ensure the return code is a 400 bad request if a duplicate email entry is detected

    """
    Login token tests
    """
    def test_login_returns_token(self):
        create_user(self.user_payload["email"], self.user_payload["username"], self.user_payload["password"]) # Create user directly in the DB based on our setup mock payload

        res = self.client.post(self.login_url, {
            "email": self.user_payload["email"],
            "password": self.user_payload["password"],
        }, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK) # Ensure a 200 status code response from server

        # Check if access or refresh (JWT tokens) exist in the response data
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    """
    Authenticated tests
    """
    def test_get_current_user_requires_auth(self):
        res = self.client.get(self.me_url) # Attempt to get a me/ url without authorization header

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) # Expect to get a 401 unauthorized response

    def test_get_current_user_returns_user(self):
        create_user(self.user_payload["email"], self.user_payload["username"], self.user_payload["password"]) # Create user directly in the DB based on our setup mock payload

        login_res = self.client.post(self.login_url, {
            "email": self.user_payload["email"],
            "password": self.user_payload["password"],
        },format="json")

        access_token = login_res.data["access"]

        self.client.credentials( # Attach the token to future requests
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        me_res = self.client.get(self.me_url) # Call the /me endpoint

        self.assertEqual(me_res.status_code, status.HTTP_200_OK) # Verify response is 200 ok

        self.assertEqual(me_res.data["email"], self.user_payload["email"]) # Verify the response user is the same as the current user payload

    """
    Logout tests:
        - Client will log in, obtain a refresh token
        - Attempts to refresh access token while logged in
        - Client calls /logout/ with current refresh token
        - Attempt to refresh again with the same token should return 401 unauthorized error
    """
    def test_logout_revokes_refresh_token(self):
        create_user(self.user_payload["email"], self.user_payload["username"], self.user_payload["password"]) # Create user directly in the DB based on our setup mock payload

        me_res = self.client.get(self.me_url) # Make a get request to the /api/v1/auth/me
        self.assertEqual(me_res.status_code, status.HTTP_401_UNAUTHORIZED) # Ensure we get an unauthorized error on the /api/v1/auth/me/ endpoint before logged in

        access, refresh = login_and_get_tokens(
            self.client, self.user_payload["email"], self.user_payload["password"], self.login_url
        )

        first_refresh = self.client.post(self.refresh_url, {"refresh": refresh}, format="json") # Make a post request to the refresh endpoint after logging in
        self.assertEqual(first_refresh.status_code, status.HTTP_200_OK) # Ensure we get a 200 ok response
        self.assertIn("access", first_refresh.data) # Ensure the response data has a new access token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}") # Add auth header to client credentials for logout

        me_res2 = self.client.get(self.me_url) # Make a get request to the /api/v1/auth/me
        self.assertEqual(me_res2.status_code, status.HTTP_200_OK) # Ensure we are getting a ok response while logged in

        logout_res = self.client.post(self.logout_url, {"refresh": refresh}, format="json")
        self.assertEqual(logout_res.status_code, status.HTTP_200_OK) # Ensure the logout endpoint returned a ok response

        second_refresh = self.client.post(self.refresh_url, {"refresh": refresh}, format="json")
        self.assertEqual(second_refresh.status_code, status.HTTP_401_UNAUTHORIZED) # Ensure the second refresh is unauthorized to indicate the user is logged out

    """
    Change password test:
        - Create a user
        - User must be authenticated
        - Old password must be correct
        - New password should replace the old one in db
        - User should be able to login with the new password
        - User should NOT be able to login with the old password
        - Ensure we get a response back 200 ok
    """
    def test_change_password(self):
        create_user(self.user_payload["email"], self.user_payload["username"], self.user_payload["password"]) # Create the mock user

        access, refresh = login_and_get_tokens(self.client, self.user_payload["email"], self.user_payload["password"], self.login_url) # Simulate a login and return of the access and refresh tokens

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}") # Attach the authorization header to simulate a logged in state

        new_password = "NewStrongPass123!"

        update_res = self.client.post(self.change_password_url, { # Test the password changing endpoint with the old and new password payload
            "old_password": self.user_payload["password"],
            "new_password": new_password,
        }, format="json")

        self.assertEqual(update_res.status_code, status.HTTP_200_OK) # Ensure the endpoint returns a 200 ok response

        self.client.credentials() # Simulate a fresh login attempt

        new_access, new_refresh = login_and_get_tokens(self.client, self.user_payload["email"], new_password, self.login_url)

        self.assertTrue(new_access)
        self.assertTrue(new_refresh)
        self.assertNotEqual(access, new_access)
        self.assertNotEqual(refresh, new_refresh)

    """
    Change password with wrong old password
        - Create a user
        - Login with the user and get token
        - Check that the access token and refresh token exist after login
        - Use change-password endpoint to update the current user's password with incorrect old password
          - Return a 400 bad request
        - Old password still works after bad request
    """
    def test_change_password_with_wrong_old_password(self):
        wrong_password="totally_wrong123"

        create_user(
            self.user_payload["email"],
            self.user_payload["username"],
            self.user_payload["password"],
            )
        
        access, refresh = login_and_get_tokens(
            self.client,
            self.user_payload["email"],
            self.user_payload["password"],
            self.login_url
            )
        
        self.assertTrue(access) # Ensure that the login provided a access token
        self.assertTrue(refresh) # Ensure that the login provided a refresh token

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        update_res = self.client.post(
            self.change_password_url,
            {
                "old_password": wrong_password,
                "new_password": "password123"
            },
            format="json"
            )

        self.assertEqual(update_res.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.credentials()
        post_change_login_res = self.client.post(
            self.login_url,
            {
                "email": self.user_payload["email"],
                "password": self.user_payload["password"]
            },
            format="json"
            )
        
        self.assertEqual(post_change_login_res.status_code, status.HTTP_200_OK) # Ensure the login is returning ok after a failed password change
        self.assertIn("access", post_change_login_res.data)

    """
    Test updating username for a user
    """
    def test_updating_username_success(self):
        create_user(
            self.user_payload["email"],
            self.user_payload["username"],
            self.user_payload["password"]
        )

        access, refresh = login_and_get_tokens(
            self.client,
            self.user_payload["email"],
            self.user_payload["password"],
            self.login_url
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        new_username="sungjinwong"

        update_username_res = self.client.post(
            self.update_username_url,
            {
                "username": new_username
            },
            format="json"
            )

        self.assertEqual(update_username_res.status_code, status.HTTP_200_OK) # Ensure 200 ok response after update
        self.assertEqual(update_username_res.data["username"], new_username)

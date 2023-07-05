from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.state import token_backend

from .models import *


class AccountModelTests(TestCase):
    def test_User(self):
        User.objects.create_user(
            "khaled", email="khaled@email.com", password="1234@#$%"
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username="khaled").role, "buyer")


class AccountAPIViewTests(APITestCase):
    login_url = reverse("accounts:token")

    def setUp(self):
        self.data = {
            "first_name": "Khaled",
            "last_name": "Nur",
            "username": "khaled",
            "email": "khaled@email.com",
            "password": "12345!@#$",
            "role": "buyer",
        }
        self.user = User.objects.create_user(
            self.data["username"],
            email=self.data["email"],
            password=self.data["password"],
            first_name=self.data["first_name"],
            last_name=self.data["last_name"],
        )

    def login(self):
        response = self.client.post(self.login_url, self.data, format="json")
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

    def test_buyer_signup(self):
        buyer_sigup_url = reverse("accounts:buyer_signup")

        # create with all correct data
        data = {
            "username": "khaled1",
            "email": "khaled1@email.com",
            "password": "12345!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"success": "User created Successfully"})
        user = User.objects.get(username=data["username"])
        self.assertEqual(user.role, "buyer")

        # create with existing username
        data = {
            "username": "khaled1",
            "email": "khaled3@email.com",
            "password": "12345!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Username already exists"})

        # create with existing email
        data = {
            "username": "khaled2",
            "email": "khaled1@email.com",
            "password": "12345!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Email already exists"})

        # create with unmatched password
        data = {
            "username": "khaled3",
            "email": "khaled3@email.com",
            "password": "123456!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # create with invalid email
        data = {
            "username": "khaled4",
            "email": "khaled3email.com",
            "password": "123456!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seller_signup(self):
        buyer_sigup_url = reverse("accounts:seller_signup")

        # create with all correct data
        data = {
            "username": "khaled1",
            "email": "khaled1@email.com",
            "password": "12345!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"success": "User created Successfully"})
        user = User.objects.get(username=data["username"])
        self.assertEqual(user.role, "seller")

        # create with existing username
        data = {
            "username": "khaled1",
            "email": "khaled3@email.com",
            "password": "12345!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Username already exists"})

        # create with existing email
        data = {
            "username": "khaled2",
            "email": "khaled1@email.com",
            "password": "12345!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Email already exists"})

        # create with unmatched password
        data = {
            "username": "khaled3",
            "email": "khaled3@email.com",
            "password": "123456!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # create with invalid email
        data = {
            "username": "khaled4",
            "email": "khaled3email.com",
            "password": "123456!@#$",
            "password2": "12345!@#$",
        }

        response = self.client.post(buyer_sigup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token(self):
        response = self.client.post(self.login_url, self.data, format="json")
        access = response.data["access"]
        refresh = response.data["refresh"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, self.data["username"])
        self.assertEqual(token_backend.decode(access)["user_id"], str(self.user.id))
        self.assertEqual(token_backend.decode(refresh)["user_id"], str(self.user.id))

    def test_get_new_access_token_providing_refresh_token(self):
        response = self.client.post(self.login_url, self.data, format="json")
        refresh = response.data["refresh"]

        token_refresh_url = reverse("accounts:token_refresh")
        response = self.client.post(token_refresh_url, {"refresh": refresh})
        access = response.data["access"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(token_backend.decode(access)["user_id"], str(self.user.id))

    def test_change_password(self):
        change_password_url = reverse("accounts:change_password")

        # without login
        data = {
            "current_password": self.data["password"],
            "new_password": "12345!@#$",
            "confirm_password": "12345!@#$",
        }
        response = self.client.patch(change_password_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.login()

        # correct all password
        data = {
            "current_password": self.data["password"],
            "new_password": "123456!@#$",
            "confirm_password": "123456!@#$",
        }
        response = self.client.patch(change_password_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, {"success": "Password Updated"})
        self.assertEqual(
            User.objects.get(username=self.data["username"]).check_password(
                data["new_password"]
            ),
            True,
        )
        self.assertNotEqual(
            User.objects.get(username=self.data["username"]).check_password(
                data["current_password"]
            ),
            True,
        )

        # incorrect current password
        data = {
            "current_password": "fhtrj",
            "new_password": "123456!@#$",
            "confirm_password": "123456!@#$",
        }
        response = self.client.patch(change_password_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # incorrect new password
        data = {
            "current_password": self.data["password"],
            "new_password": "123456!@#$",
            "confirm_password": "12345!@#$",
        }
        response = self.client.patch(change_password_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_data(self):
        self.login()
        user_data_url = reverse("accounts:data")

        response = self.client.get(user_data_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.data.pop("password")
        self.assertEqual(response.data, self.data)

    def test_check_password(self):
        self.login()
        check_password_url = reverse("accounts:check_password")

        data = {"password": self.data["password"]}
        response = self.client.post(check_password_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"success": "Correct password"})

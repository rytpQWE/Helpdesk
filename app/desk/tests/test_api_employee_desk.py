from unittest import TestCase

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse

EMPLOYEE_DESK_URL = reverse('employee-list')


class PublicUserDeskApiTest(TestCase):
    """
    Testing unauthenticated recipe API request
    """

    def setUp(self):
        self.client = APIClient()

    def test_account_auth_required(self):
        response = self.client.get(EMPLOYEE_DESK_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserNoPermissionApiTest(APITestCase):
    """
    Testing authenticated user without permission
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='testpassword',
            email='example@mail.ru'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_auth_user_no_permission(self):
        response = self.client.get(EMPLOYEE_DESK_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivateUserHavePermissionApiTest(APITestCase):
    """
    Testing authenticated user with permission
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='testpassword',
            email='example@mail.ru',
        )
        self.user.employee.is_employee = True
        self.user.employee.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_auth_user_with_permission(self):
        response = self.client.get(EMPLOYEE_DESK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

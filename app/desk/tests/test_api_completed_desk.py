from unittest import TestCase

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse

COMPLETED_DESK_URL = reverse('desk_completed-list')


class PublicUserDeskApiTest(TestCase):
    """
    Testing unauthenticated recipe API request
    """

    def setUp(self):
        self.client = APIClient()

    def test_account_no_auth_required(self):
        response = self.client.get(COMPLETED_DESK_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserDeskApiTest(APITestCase):
    """
    Testing authenticated API access
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='testpassword',
            email='example@mail.ru'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_account_no_auth_required(self):
        response = self.client.get(COMPLETED_DESK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from django.contrib.auth.models import User
from unittest import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

import celery
from desk.models import Category, Desk
from desk.serializers import DeskCreateSerializer
from desk.tasks import send_employee_mail

DESK_URL_LIST = reverse('main-list')


class PublicUserDeskApiTest(TestCase):
    """
    Testing unauthenticated recipe API request
    """

    def setUp(self):
        self.client = APIClient()

    def test_account_no_auth_required(self):
        response = self.client.get(DESK_URL_LIST)
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
        self.category = Category.objects.create(category='test')
        self.serializer_data = {
            'User': self.user,
            'title': 'test',
            'category': self.category,
            'comment': 'test',
        }
        self.ticket = Desk.objects.create(**self.serializer_data)

    def test_getlist_auth_user(self):
        response = self.client.get(DESK_URL_LIST)
        ticket = Desk.objects.all()
        serializer_data = DeskCreateSerializer(ticket, many=True).data
        self.assertEqual(serializer_data, response.data['results'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket(self):
        payload = {
            'User': self.user.id,
            'title': 'test',
            'category': self.category.id,
            'comment': 'test',
        }
        response = self.client.post(DESK_URL_LIST, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_object(self):
        url = reverse('main-detail', args={self.ticket.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ticket(self):
        url = reverse('main-detail', args={self.ticket.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_check_status_task_celery(self):
        task = send_employee_mail.delay(1)
        result = celery.result.AsyncResult(task.id)
        self.assertEqual(result.status, 'PENDING')

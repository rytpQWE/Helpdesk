import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from desk.models import Desk, Category, DeskImage
from desk.serializers import DeskCreateSerializer, ImagesSerializer


class ImagesSerializerTestCase(TestCase):
    def test_image(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        category = Category.objects.create(category='test')
        serializer_data_desk = {
            'User': user,
            'title': 'test',
            'category': category,
            'comment': 'test',
        }
        url_image = 'imagetest.png'
        desk = Desk.objects.create(**serializer_data_desk)
        serializer_data_images = {
            'desk': desk,
            'images': url_image
        }
        image_obj = DeskImage.objects.create(**serializer_data_images)
        data = ImagesSerializer([image_obj], many=True).data
        expected_data = [{
            'images': f'/media/{url_image}'
        }]
        self.assertEqual(data, expected_data)


class DeskCreateSerializerTestCase(TestCase):
    def test_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        category = Category.objects.create(category='test')
        serializer_data = {
            'User': user,
            'title': 'test',
            'category': category,
            'comment': 'test',
        }
        mocked = datetime.datetime(9999, 9, 9, 0, 0, 0,).strftime("%Y-%d-%m %H:%M:%S")
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            ticket = Desk.objects.create(**serializer_data)
            data = DeskCreateSerializer([ticket], many=True).data
            expected_data = [{
                'id': ticket.id,
                'User': user.id,
                'title': 'test',
                'category': category.id,
                'comment': 'test',
                'status': 'accepted',
                'images_set': [],
                'created_at':mocked,
            }]
            self.assertEqual(data, expected_data)


class DeskCompleteSerializerTestCase(TestCase):
    def test_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        category = Category.objects.create(category='test')
        serializer_data = {
            'User': user,
            'title': 'test',
            'category': category,
            'comment': 'test',
            'status': 'completed'
        }
        mocked = datetime.datetime(9999, 9, 9, 0, 0, 0, ).strftime("%Y-%d-%m %H:%M:%S")
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            ticket = Desk.objects.create(**serializer_data)
            data = DeskCreateSerializer([ticket], many=True).data
            expected_data = [{
                'id': ticket.id,
                'User': user.id,
                'title': 'test',
                'category': category.id,
                'comment': 'test',
                'status': 'completed',
                'images_set': [],
                'created_at': mocked,
            }]
            self.assertEqual(data, expected_data)


class EmployeeDeskSerializerTestCase(TestCase):
    def test_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        category = Category.objects.create(category='test')
        serializer_data = {
            'User': user,
            'title': 'test',
            'category': category,
            'comment': 'test',
        }
        mocked = datetime.datetime(9999, 9, 9, 0, 0, 0, ).strftime("%Y-%d-%m %H:%M:%S")
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            ticket = Desk.objects.create(**serializer_data)
            data = DeskCreateSerializer([ticket], many=True).data
            expected_data = [{
                'id': ticket.id,
                'User': user.id,
                'title': 'test',
                'category': category.id,
                'comment': 'test',
                'status': 'accepted',
                'images_set': [],
                'created_at': mocked,
            }]
            self.assertEqual(data, expected_data)
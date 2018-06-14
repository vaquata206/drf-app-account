from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'admin',
            'password': 'unknown'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        """login"""
        response = self.client.post('/api/login/', data=self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RegisterInTest(TestCase):
    def setUp(self):
        self.user = {
            'username': 'admin2',
            'password': 'unknown@123',
            'password_2': 'unknown@123',
            'email': 'unknown2@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        self.user_exist = {
            'username': 'admin1',
            'password': 'unknown@123',
            'email': 'unknown1@gmail.com',
            'first_name': 'unknown',
            'last_name': 'unknown'
        }

        User.objects.create_user(**self.user_exist)

    def test_register(self):
        """register"""
        response = self.client.post('/api/register/', data=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_exist(self):
        """case: register a user that is exist"""
        response = self.client.post('/api/register/', data=self.user_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


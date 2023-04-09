from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_AUTH_URL = reverse('user:token')

def create_user(**payload):
    get_user_model().objects.create_user(**payload)

class PublicUserAPITest(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test user'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test user'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_short_password_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'ps',
            'name': 'Test user'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_successful(self):
        user_payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test user'
        }
        create_user(**user_payload)

        token_payload = {
            'email': user_payload['email'],
            'password': user_payload['password']
        }
        res = self.client.post(TOKEN_AUTH_URL, token_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_bad_credentials(self):
        create_user(email='test@example.com', password='correctPass123')

        payload = {
            'email': 'test@example.com',
            'password': 'wrongPass123'
        }

        res = self.client.post(TOKEN_AUTH_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
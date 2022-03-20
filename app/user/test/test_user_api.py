from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API public"""

    def setUp(self) -> None:
        self.client = APIClient()
        return super().setUp()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'user@gmail.com',
            'password': '123456',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exits(self):
        """test creating user that already exist"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'testpass'
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more that 5 character"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'asw',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_toen_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'user@gmail.com',
            'password': 'testpassword'
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """Test that token in not created if invalid credential"""
        get_user_model().objects.create_user(email='test@gmail.com', password='testpass')
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrongasd'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token in not created if user dont exist"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrongasd'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

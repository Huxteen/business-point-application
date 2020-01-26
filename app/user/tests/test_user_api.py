from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
  return User.objects.create_user(**params)


class PublicUserApiTest(TestCase):
  """Test users API (public)"""

  def setUp(self):
    self.client = APIClient()

  def test_create_valid_user_success(self):
    """Test creating user with valid payload is successful"""

    payload = {
      'email': 'test@gmail.com',
      'password': 'austin12345',
      'name': 'Austin Smith'
    }

    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(**res.data)
    self.assertTrue(user.check_password(payload['password']))
    self.assertNotIn('password', res.data)

  def test_user_exists(self):
    """Test to check if user already created."""

    payload = {'email':'test@gmail.com', 'password':'austin12345'}
    create_user(**payload)

    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_password_too_short(self):
    """Password must be more than 8 characters."""
    payload = {'email':'test@gmail.com', 'password': 'pw'}
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    user_exists = User.objects.filter(
      email=payload['email']
    ).exists()
    self.assertFalse(user_exists)


  def test_create_token_for_user(self):
    """Test that a token is created for the user."""

    payload = {'email':'test@gmail.com', 'password':'austin12345'}
    create_user(**payload)
    res = self.client.post(TOKEN_URL, payload)
    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_create_token_invalid_credentials(self):
    """Test that token is not created if invalid credentials are given"""
    payload = {'email':'test@gmail.com', 'password':'missit'}
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


  def test_create_token_no_user(self):
    """Test that token is not created if user doesnot exist."""
    payload = {'email':'test@gmail.com', 'password':'austin12345'}
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


  def test_create_token_missing_field(self):
    """Test that email and password are required."""
    payload = {'email':'test@gmail.com', 'password':''}
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




    
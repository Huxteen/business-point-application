from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from post.serializers import TagSerializer

TAGS_URL = reverse('post:tag-list')


class PublicTagsApiTests(TestCase):
  """Test the publicly available tags API."""

  def setUp(self):
    self.client = APIClient()

  def test_login_required(self):
    """ Test that login is required for retrieving tags"""
    res = self.client.get(TAGS_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
  """Test the authorized user tags API."""

  def setUp(self):
    self.user = User.objects.create_user(
      'test@gmail.com',
      'austin12345'
    )

    self.client = APIClient()
    self.client.force_authenticate(self.user)

  def test_retrieve_tags(self):
    """Test retrieveing tags."""
    Tag.objects.create(user=self.user, name='Nigeria')
    Tag.objects.create(user=self.user, name='Lagos')

    res = self.client.get(TAGS_URL)

    tags = Tag.objects.all().order_by('-name')
    serializer = TagSerializer(tags, many=True)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)


  def test_tags_limited_to_user(self):
    """Test that tags returned are for the authorized user."""
    another_user = User.objects.create_user(
      'anothertest@gmail.com',
      'austin45678'
    )
    Tag.objects.create(user=another_user, name='Abuja')
    tag = Tag.objects.create(user=self.user, name='Ogun Nigeria')

    res = self.client.get(TAGS_URL)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data[0]['name'], tag.name)


  def test_create_tag_successful(self):
    """Test creating a new tag."""
    payload = {'name': 'Test tag'}
    self.client.post(TAGS_URL, payload)

    exists = Tag.objects.filter(
      user=self.user,
      name=payload['name']
    ).exists()
    self.assertTrue(exists)

  
  def test_create_tag_invalid(self):
    """Test creating a new tag with invalid payload."""
    payload = {'name': ''}
    res = self.client.post(TAGS_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
  Post,
  Tag
)

from post.serializers import (
  PostSerializer, 
  PostDetailSerializer
)


POST_URL = reverse('post:post-list')

def detail_url(post_id):
  """Return post detail URL."""
  return reverse('post:post-detail', args=[post_id])


def sample_tag(user, name='Finance'):
  """Create and return a sample tag."""
  return Tag.objects.create(user=user, name=name)


def sample_post(user_id, **params):
  """Create and return a sample post."""
  defaults = {
    'title': 'sample post',
    'body': 'Hello our sample post body'
  }
  defaults.update(params)

  return Post.objects.create(user_id=user_id, **defaults)


class PublicPostApiTests(TestCase):
  """Test if post is retrieved from API."""

  def setUp(self):
    self.client = APIClient()


class PrivatePostApiTests(TestCase):
    """Test authenticated post API access"""

    def setUp(self):
      self.client = APIClient()
      self.user = User.objects.create_user(
          'test@gmail.com',
          'austin12345'
      )
      self.client.force_authenticate(self.user)

    def test_retrieve_post(self):
      """Test retrieving list of posts"""
      # sample_post(user_id=self.user)
      # sample_post(user_id=self.user)

      res = self.client.get(POST_URL)

      posts = Post.objects.all().order_by('-id')
      serializer = PostSerializer(posts, many=True)
      self.assertEqual(res.status_code, status.HTTP_200_OK)
      self.assertEqual(res.data, serializer.data)

    def test_view_post_detail(self):
      """Test viewing a post detail"""
      post = sample_post(user_id=self.user)
      post.tags.add(sample_tag(user=self.user))

      url = detail_url(post.id)
      res = self.client.get(url)

      serializer = PostDetailSerializer(post)
      self.assertEqual(res.data, serializer.data)


    

















    
































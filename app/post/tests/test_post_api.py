from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post

from post.serializers import PostSerializer

POST_URL = reverse('post:post-list')

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
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test@gmail.com',
            'austin12345'
        )
        self.client.force_authenticate(self.user)

    # def test_retrieve_post(self):
    #     """Test retrieving list of posts"""
    #     sample_post(user_id=self.user)
    #     sample_post(user_id=self.user)

    #     res = self.client.get(POST_URL)

    #     posts = Post.objects.all().order_by('-id')
    #     serializer = PostSerializer(posts, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    

















    
































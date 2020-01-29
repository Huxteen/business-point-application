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
    'title': 'sample post demo',
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

    
    def test_create_post(self):
      """Test creating post"""
      payload = {
        'user_id': self.user.id,
        'title': 'How the world evolve',
        'body': 'This is a demonstration on how the world eveolved'
      }
      res = self.client.post(POST_URL, payload)

      self.assertEqual(res.status_code, status.HTTP_201_CREATED)
      post = Post.objects.get(id=res.data['id'])
      self.assertEqual(post.title, payload['title'])
      self.assertEqual(post.body, payload['body'])
      self.assertEqual(post.user_id.id, payload['user_id'])
      

    def test_create_post_with_tag(self):
      """Test creating a post with tags."""
      tag1 = sample_tag(user=self.user, name='Ikeja')
      tag2 = sample_tag(user=self.user, name='Lekki')

      payload = {
        'user_id': self.user.id,
        'title': 'Places in Nigeria.',
        'tags': [tag1.id, tag2.id],
        'body': 'The nature of the Country'
      }
      res = self.client.post(POST_URL, payload)

      self.assertEqual(res.status_code, status.HTTP_201_CREATED)
      post = Post.objects.get(id=res.data['id'])
      tags = post.tags.all()
      self.assertEqual(tags.count(), 2)
      self.assertIn(tag1, tags)
      self.assertIn(tag2, tags)

    def test_partial_update_post(self):
      """Test updating a post with patch."""
      post = sample_post(user_id=self.user)
      post.tags.add(sample_tag(user=self.user))
      new_tag = sample_tag(user=self.user, name='Blockchain')

      payload = {
        'title': 'Environment variable',
        'tags': [new_tag.id]
      }
      url = detail_url(post.id)
      self.client.patch(url, payload)

      post.refresh_from_db()
      self.assertEqual(post.title, payload['title'])
      tags = post.tags.all()
      self.assertEqual(len(tags), 1)
      self.assertIn(new_tag, tags)


    def test_full_update_post(self):
      """Test updating a post with put."""
      post = sample_post(user_id=self.user)
      post.tags.add(sample_tag(user=self.user))
      new_tag = sample_tag(user=self.user, name='Crypto currency')
      payload = {
        'user_id': self.user.id,
        'title':'We love to code',
        'body': 'coding is a fun event that keeps you always eager to learn new technology',
        'tags': [new_tag.id]
      }
      url = detail_url(post.id)
      self.client.put(url, payload)
      
      post.refresh_from_db()
      self.assertEqual(post.title, payload['title'])
      self.assertEqual(post.body, payload['body'])

      tags = post.tags.all()
      self.assertEqual(len(tags), 1)

    
    def test_filter_post_by_title(self):
      """Test returning post searched post."""
      post1 = sample_post(user_id=self.user, title="Hello programmer")
      post2 = sample_post(user_id=self.user, title="We love programmer")
      post3 = sample_post(user_id=self.user, title="The code defines you")
      tag1 = sample_tag(user=self.user, name="Finance")
      tag2 = sample_tag(user=self.user, name="Technology")
      post1.tags.add(tag1)
      post2.tags.add(tag2)
      post3.tags.add(tag1)

      res = self.client.get(
        POST_URL,
        {'search':f'programmer'}
      )

      serializer1 = PostSerializer(post1)
      serializer2 = PostSerializer(post2)
      serializer3 = PostSerializer(post3)

      self.assertIn(serializer1.data, res.data)
      self.assertIn(serializer2.data, res.data)
      self.assertNotIn(serializer3.data, res.data)








    

















    
































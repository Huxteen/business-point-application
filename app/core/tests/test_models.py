from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from core import models



def sample_user(email='test@gmail.com', password='austin12345'):
  """Create a sample user"""
  return User.objects.create_user(email, password)


class ModelTests(TestCase):

  def test_create_user_with_email_successful(self):
    """Test creating a new user with an email is successful"""
    email = 'test@gmail.com'
    password = "austin12345"
    user = User.objects.create_user(
        email=email,
        password=password
    )

    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))


  def test_new_user_email_normalized(self):
    """Test the email for a new user is normalized"""
    email = "test@gmail.com"
    user = get_user_model().objects.create_user(email, 'austin12345')
    self.assertEqual(user.email, email.lower())

  def test_new_user_invalid_email(self):
    """Test creating user with no email raise error."""
    with self.assertRaises(ValueError):
      User.objects.create_user(None, 'austin12345')

  def test_create_new_superuser(self):
    """Test creating a new superuser"""
    user = User.objects.create_superuser(
        'test@gmail.com',
        'austin12345'
    )
    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)


  def test_tag_str(self):
    """Test the tag string representation."""
    tag = models.Tag.objects.create(
      user=sample_user(),
      name='Nigeria'
    )
    
    self.assertEqual(str(tag), tag.name)
  

  def test_post_str(self):
    """Test the post string representation."""
    post = models.Post.objects.create(
      user_id=sample_user(),
      title='Circular Economy:Tackling electronic waste in Nigeria',
      body='We discuss Nigeria e-waste problem and how recycling and circularity can solve it',
    )
    self.assertEqual(str(post), post.title)


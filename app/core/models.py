from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
      """Create and save a new user"""
      if not email:
          raise ValueError('User must have an email address')
      user = self.model(email=self.normalize_email(email), **extra_fields)
      user.set_password(password)
      user.save(using=self._db)

      return user

    def create_superuser(self, email, password):
      """Create and saves a new super user"""
      user = self.create_user(email, password)
      user.is_staff = True
      user.is_superuser = True
      user.save(using=self._db)

      return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'



class Tag(models.Model):
  """Tag to be used for a Post."""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True) 
  modified = models.DateTimeField(auto_now=True) 

  def __str__(self):
    return self.name

class Post(models.Model):
  """Post Object."""
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  # url = models.SlugField(max_length=40)
  title = models.CharField(max_length=255)
  body = models.TextField()
  #tags = models.CharField(max_length=255)
  created = models.DateTimeField(auto_now_add=True) 
  modified = models.DateTimeField(auto_now=True)
  tags = models.ManyToManyField('Tag')

  def __str__(self):
    return self.title

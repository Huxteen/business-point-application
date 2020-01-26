from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  """Serializer for User Objects"""
  class Meta:
    model = User
    fields = ('email', 'password','name')
    extra_kwargs = {'password': {'write_only': True, 'min_length':8}}

  def create(self, validated_data):
    """Create a new user with encrypted password and return it."""

    return User.objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
  """Serializer for the user authentication object."""
  email = serializers.CharField()
  password = serializers.CharField(
    style={'input_type':'password'},
    trim_whitespace=False
  )

  def validate(self, params):
    """Validate and authenticate the user."""
    email = params.get('email')
    password = params.get('password')

    user = authenticate(
      request=self.context.get('request'),
      username=email,
      password=password
    )

    if not user:
      msg = _('Email or password do not match our records.')
      raise serializers.ValidationError(msg, code='authentication')

    params['user'] = user
    return params





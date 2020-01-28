from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post, Tag
from post import serializers

# Create your views here.

class TagViewSet(viewsets.GenericViewSet, 
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
  """Manage tag in the database."""
  serializer_class = serializers.TagSerializer
  queryset = Tag.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    """retrieve tag for the current authenticated user."""
    return self.queryset.filter(user=self.request.user).order_by('-name')

  def perform_create(self, serializer):
    """Create new tag"""
    serializer.save(user=self.request.user)





class PostViewSet(viewsets.ModelViewSet):
  """Manage post in the database."""
  serializer_class = serializers.PostSerializer
  queryset = Post.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    """retrieve the all post."""
    return self.queryset.filter(user_id=self.request.user)

  





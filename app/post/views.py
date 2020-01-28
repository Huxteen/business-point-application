from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post
from post import serializers

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
  """Manage post in the database."""
  serializer_class = serializers.PostSerializer
  queryset = Post.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    """retrieve the all post."""
    return self.queryset.filter(user=self.request.user)

  





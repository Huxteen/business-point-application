from rest_framework import serializers 
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
  """Serialize a post."""

  
  class Meta:
    model = Post
    fields = (
      'id', 'user_id', 'title', 'body',
      'created', 'modified', 'tags'
    )
    read_only_fields = ('id',)

from rest_framework import serializers 
from core.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
  """Serialize for Tag object."""

  class Meta:
    model = Tag
    fields = ('id', 'name')
    read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
  """Serialize a post."""
  tags = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=Tag.objects.all()
  )

  class Meta:
    model = Post
    fields = (
      'id', 'user_id', 'title', 'body',
      'created', 'modified', 'tags'
    )
    read_only_fields = ('id',)

  
class PostDetailSerializer(PostSerializer):
  """Serialize a post detail."""
  tags = TagSerializer(many=True, read_only=True)

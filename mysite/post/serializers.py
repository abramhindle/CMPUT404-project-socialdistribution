from rest_framework import serializers

from user.serializers import AuthorSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

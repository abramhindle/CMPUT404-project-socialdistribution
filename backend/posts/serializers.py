from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["type", "title", "id", "source", "origin", "description", "comments", "contentType", "content", "author", "categories", "published", "visibility", "unlisted"]

from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer

class PostReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Post
        #TODO add comments
        fields = ["type", "title", "id", "source", "origin", "description", "contentType", "content", "author", "categories", "published", "visibility", "unlisted"]
        depth = 1

class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        #TODO add comments
        fields = ["type", "title", "id", "source", "origin", "description", "contentType", "content", "author", "categories", "published", "visibility", "unlisted"]
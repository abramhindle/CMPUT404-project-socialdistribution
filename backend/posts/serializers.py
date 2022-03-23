from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["type", "title", "id", "source", "origin", "description", "comments", "contentType", "content", "author", "categories", "published", "visibility", "unlisted"]

    def get_comments(self, obj: Post):
        return f"{obj.id}/comments/"

from backend.helpers import get
from rest_framework import serializers
from comment.models import Comment
import requests as r


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        write_only_fields = ["local_id", "post"]
        read_only_fields = ["author"]
        fields = ["type", "author", "comment", "contentType", "published", "id"]

    def get_author(self, obj: Comment):
        author_url = obj.author_url
        author = get(author_url)
        return author.json() if author is not None else {"error": "Author Not Found!"}

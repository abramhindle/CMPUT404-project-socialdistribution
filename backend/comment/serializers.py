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
        return r.get(author_url).json()

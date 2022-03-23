from rest_framework import serializers
from likes.models import Likes
import requests as r


class LikesSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Likes
        fields = ["type", "summary", "context", "object", "author"]

    def get_author(self, obj: Likes):
        author_url = obj.author_url
        return r.get(author_url).json()

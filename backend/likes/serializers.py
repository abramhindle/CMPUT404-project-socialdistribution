from rest_framework import serializers
from likes.models import Likes


class LikesSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = Likes
        fields = ["type", "summary", "context", "object", "author"]

    def get_author(self, obj: Likes):
        return obj.author_url

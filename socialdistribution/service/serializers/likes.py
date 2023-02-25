from rest_framework import serializers
from service.models.likes import Likes
from service.serializers.author import AuthorSerializer


class LikesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
    
    class Meta:
        model = Likes
        fields = ("type", "context", "summary", "author", "object",)
        
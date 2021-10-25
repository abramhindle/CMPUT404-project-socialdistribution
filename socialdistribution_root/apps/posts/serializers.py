# Implementation of serializers from the tutorial: https://www.django-rest-framework.org/tutorial/1-serialization/

from rest_framework import serializers
from apps.posts.models import Post
from apps.core.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_post_id", read_only=True)
    type = serializers.CharField(default="post", read_only=True)
    author = UserSerializer(read_only=True)


    class Meta:
        model = Post
        fields = [
            'type', 
            'title', 
            'id', 
            'description',
            'author',
            'published',
            'visibility'
        ]
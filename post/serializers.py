from django.db import models
from .models import Post,Like,Comment
from rest_framework import serializers
from author.serializers import AuthorSerializer

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_url", read_only=True)
    url = serializers.CharField(source="get_url", read_only=True)
    type = serializers.CharField(default="post", read_only=True)
    author = AuthorSerializer(source="ownerID")
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'content-type', 'isPublic', 'isListed', 'hasImage', 'host', 'url', 'type']
        extra_kwargs = {
            # rename contentType to content-type
            'content-type': {'source': 'contentType'},
        }

class LikeSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(source="get_id", read_only=True)
    #url = serializers.CharField(source="get_url", read_only=True)
    type = serializers.CharField(default="like", read_only=True)
    author = AuthorSerializer(source="authorID")
    post = PostSerializer(source="postID")
    date = serializers.DateTimeField(source="get_date", read_only=True)
    class Meta:
        model = Like
        fields = ['author','post','date','type']
        

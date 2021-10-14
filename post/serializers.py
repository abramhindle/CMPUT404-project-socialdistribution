from django.db import models
from .models import Post,Like,Comment
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_url", read_only=True)
    url = serializers.CharField(source="get_url", read_only=True)
    type = serializers.CharField(default="post", read_only=True)
    class Meta:
        model = Post
        fields = ['id','author','content','content-type','isPublic','isListed','hasImage','host','url','type']

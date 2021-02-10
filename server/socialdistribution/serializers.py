from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'postID', 'source', 'origin', 'description', 'contentType', 
            'content', 'count', 'size', 'comments', 'published', 'visibility', 'unlisted']
from rest_framework import serializers
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    pass
#     class Meta:
#         model = Author
#         fields = ['authorID', 'host', 'displayName', 'url', 'github']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'postID', 'source', 'origin', 'description', 'contentType', 
            'content', 'count', 'size', 'comments', 'published', 'visibility', 'unlisted']
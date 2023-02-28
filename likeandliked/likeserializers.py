from rest_framework import serializers
from .models import Post, Comment, Like

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'url', 'github', 'profileImage']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'published', 'author', 'categories', 'visibility', 'unlisted']

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'published', 'author', 'post']

class LikeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Like
        fields = ['id', 'author', 'object', 'published']

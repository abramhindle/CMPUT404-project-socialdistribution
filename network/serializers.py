from rest_framework import serializers
from network.models import Author, Post, Comment

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage']  

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['type', 'id', 'title', 'description', 'author','visibility', 'origin'] 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'published', 'id'] 




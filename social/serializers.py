from rest_framework import serializers
from .models import Author, Post, Comment

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id','host','displayName','url','github_url')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','url','title','source','origin','description',
                  'contentType','content','author','published','visibility','unlisted')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','post','author','contentType','comment','published')

from rest_framework import serializers
from .models import *

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['authorID', 'email', 'username', 'password', 'github']
    
    def save(self):
        author = Author(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            github=self.validated_data['github']
        )
        password = self.validated_data['password']
        author.set_password(password)
        author.save()
        return author


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='get_id')
    host = serializers.URLField(source='get_host')
    displayName = serializers.CharField(source='username')
    url = serializers.CharField(source='get_id')

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'url', 'github']


class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='get_post_id', required=False)
    comments = serializers.URLField(source='get_comments_url', required=False)

    def to_representation(self, instance):
        response = super(PostSerializer, self).to_representation(instance)
        author = Author.objects.get(authorID=instance.authorID)
        author_serializer = AuthorSerializer(author)
        del response['authorID']
        del response['postID']
        response['author'] = author_serializer.data # add author data
        
        return response

    class Meta:
        model = Post
        fields = ['title', 'id', 'authorID', 'postID', 'source', 'origin', 'description', 'contentType', 
            'content', 'count', 'comments', 'published', 'visibility', 'unlisted']

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='get_comment_id', required=False)
    author = serializers.CharField(source='get_author',required=False)
    def to_representation(self, instance):
        response = super(CommentSerializer, self).to_representation(instance)
        author = Author.objects.get(authorID=instance.authorID)
        author_serializer = AuthorSerializer(author)
        del response['authorID']
        del response['postID']
        response['author'] = author_serializer.data # add author data
        return response

    class Meta:
        model = Comment
        fields = ['model_type','id','comment','author','ContentType','published','commentID','authorID','postID']
    def get_author(self,instance):
        author_data = Author.objects.get(authorID=instance.authorID)
        author_serializer = AuthorSerializer(author_data)
        author = author_serializer.data
        return author
    


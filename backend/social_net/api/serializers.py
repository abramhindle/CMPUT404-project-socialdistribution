#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import AuthorModel, PostsModel, CommentsModel, LikeModel, FollowModel, InboxModel
from rest_framework import validators

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.URLField(required=False)
    
    class Meta:
        model = AuthorModel
        fields = ('id', 'type', 'host', 'url', 'displayName', 'github', 'profileImage', 'created_at')
    
    def create(self, validated_data):
        author = AuthorModel.objects.create(**validated_data)
        return author

class PostsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    id = serializers.URLField(required=False)
    def create(self, validated_data):
        
        author_data = validated_data.pop('author', None)
        
        author = AuthorModel.objects.get(**author_data)
        post = PostsModel.objects.create(author=author, **validated_data)
        return post
    
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        author = AuthorModel.objects.get(**author_data)
        instance.author = author
        instance.type = validated_data.get('type', instance.type)
        instance.title = validated_data.get('title', instance.title)
        instance.source = validated_data.get('source', instance.source)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.description = validated_data.get('description', instance.description)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.content = validated_data.get('content', instance.content)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.count = validated_data.get('count', instance.count)
        instance.published = validated_data.get('published', instance.published)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.id = validated_data.get('id', instance.id)
        instance.save()
        return instance

    class Meta:
        model = PostsModel
        fields = ('id', 'type', 'author', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'categories', 'count', 'published', 'visibility', 'unlisted')
        extra_kwargs = {
           'author': {
            'validators': []
            },
        }
    

    
    
class CommentsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    post = PostsSerializer(required=False)

    def create(self, validated_data):
        
        author = validated_data.pop('author')
        post = validated_data.pop('post')
        post.pop('author')
        
        author = AuthorModel.objects.get(**author)
        post = PostsModel.objects.filter(**post).first()
        
        comment = CommentsModel.objects.create(
            post=post,
            author=author,
            **validated_data)
        return comment
    
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        author = AuthorModel.objects.get(**author_data)
        instance.author = author
        instance.type = validated_data.get('type', instance.type)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.host = validated_data.get('host', instance.host)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.published = validated_data.get('published', instance.published)
        instance.save()
        return instance

    class Meta:
        model = CommentsModel
        fields = ('id', 'type', 'comment', 'host', 'contentType', 'published', 'author', 'created_at', 'post')

class LikeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = AuthorModel.objects.get(**author_data)

        like = LikeModel.objects.create(author=author, **validated_data)
        return like

    class Meta:
        model = LikeModel
        fields = ('id', 'summary', 'type', 'author', 'object', 'post', 'comment', 'created_at')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowModel
        fields = ('status', 'follower', 'following', 'created_at')


class InboxSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = AuthorModel.objects.get(**author_data)
        inbox = InboxModel.objects.create(author=author, **validated_data)
        return inbox

    class Meta:
        model = InboxModel
        fields = ('id', 'type', 'author', 'object', 'created_at')

    

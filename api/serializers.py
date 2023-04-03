#from django.contrib.auth.models import User, Group
import os
from rest_framework import serializers

from api.utils import build_url, which_node, KNOWN_TEAMS, create_author_url, create_post_url, create_comment_url
from .models import AuthorModel, PostsModel, ImageModel,  CommentsModel, LikeModel, FollowModel, InboxModel, NodeModel
from rest_framework import validators


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeModel
        fields = ['id', 'node_url', 'node_name', 'node_user', 't16_uname', 't16_pw']


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.URLField(required=False)
    
    class Meta:
        model = AuthorModel
        fields = ('id', 'type', 'host', 'url', 'displayName', 'github', 'profileImage', 'created_at')
    
    def create(self, validated_data):
        author = AuthorModel.objects.create(**validated_data)
        return author
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['url'] = repr['id']
        
        # Ensure host is the proper format without accidentally overwriting it
        # If the host field is the correct format, leave it alone
        if repr['host'] in KNOWN_TEAMS.keys():
            pass
        else:
            # Else if it is a known team in the incorrect format, fix it
            node_host = which_node(repr['id'], return_host=True)
            if node_host != 'TEAM_UNKNOWN':
                repr['host'] = node_host
                
        if KNOWN_TEAMS.get(repr['host']) == 'TEAM_16':
            repr['profileImage'] = repr['id'] + '/image'

        return repr
    
    def to_internal_value(self, data):
        data['url'] = data['id']
        
        # Ensure host is the proper format without accidentally overwriting it
        # If the host field is the correct format, leave it alone
        if data['host'] in KNOWN_TEAMS.keys():
            pass
        else:
            # Else if it is a known team in the incorrect format, fix it
            node_host = which_node(data['id'], return_host=True)
            if node_host != 'TEAM_UNKNOWN':
                data['host'] = node_host
                
        return super().to_internal_value(data)


class PostsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    id = serializers.URLField(required=False)
    def create(self, validated_data):
        
        author_data = validated_data.pop('author', None)
        
        author = AuthorModel.objects.get(id=author_data.get('id'))
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
        
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        
        
        which_team = which_node(repr.get('id'))
        
        # Don't wanna be constantly sending binary image, so replace it with the url if it's ours.
        if (which_team == 'TEAM_16') and ('image' in repr['contentType']) and ('base64' in repr['content']):
            repr['content'] = repr['id'] + '/image'
        
        # Don't want no localhost in my urls
        if 'localhost' in repr['source']:
            repr['source'] = repr['id']
        if 'localhost' in repr['origin']:
            repr['origin'] = repr['id']

        
        return repr
    
    def to_internal_value(self, data):
        # For when we're creating brand new posts
        
        if not data.get('id', ''):
            data['id'] = create_post_url(data['author']['id'])
            data['origin'] = data['id']
            data['source'] = data['id']
            
        
         # Don't want no localhost in my urls
        if 'localhost' in data['source']:
            data['source'] = data.get('id', '')
        if 'localhost' in data['origin']:
            data['origin'] = data.get('id', '')       
        
      
        return super().to_internal_value(data)



class ImageSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    post = PostsSerializer(required=False)
    
    def create(self, validated_data):
        author = validated_data.pop('author', None)
        post = validated_data.pop('post', None)
        
        if author:
            author = AuthorModel.objects.get(**author)
            image = ImageModel.object.create(author=author, **validated_data)
            return image
        
        if post:
            post = PostsModel.objects.get(**post)
            image = ImageModel.objects.create(post=post, **validated_data)
            return image
        
    class Meta:
        model = ImageModel
        fields = ('image', 'author', 'post')

    
class CommentsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    post = PostsSerializer(required=False)

    def create(self, validated_data):
        
        author = validated_data.pop('author')
        post = validated_data.pop('post')
        post.pop('author')

        author = AuthorModel.objects.get(id=author.get('id'))
        post = PostsModel.objects.get(id=post.get('id'))
        
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
    author = AuthorSerializer(required=False)
    
    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = AuthorModel.objects.get(id=author_data.get('id'))

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

        author_id = validated_data.pop('author').get('id')
        author = AuthorModel.objects.get(id=author_id)
        validated_data['author'] = author
        return super().create(validated_data)

    class Meta:
        model = InboxModel
        fields = ('id', 'type', 'author', 'object', 'created_at')
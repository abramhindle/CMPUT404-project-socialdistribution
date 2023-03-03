#from django.contrib.auth.models import User, Group
from .models import AuthorModel, PostsModel
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=100, default='')
    id = serializers.CharField(max_length=150, default='')
    url = serializers.CharField(max_length=100, default='')
    host = serializers.CharField(max_length=150,default='')
    displayName = serializers.CharField(max_length=150, default='')
    github = serializers.CharField(max_length=150, default='')
    profileImage = serializers.CharField(max_length=500, default='')

    #TODO: create a method to create a new author
    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.id = validated_data.get('id', instance.id)
        instance.url = validated_data.get('url', instance.url)
        instance.host = validated_data.get('host', instance.host)
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        return instance
    class Meta:
        model = AuthorModel
        # Tuple of serialized model fields (see link [2])
        fields = ('type', 'id', 'host', 'displayName', 'github', 'url', 'profileImage')

class PostsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=100, default='post')
    title = serializers.CharField(max_length=100, default='')
    id = serializers.CharField(max_length=100)
    source = serializers.CharField(max_length=100, default="")
    origin = serializers.CharField(max_length=100, default='')
    description = serializers.CharField(max_length=500, default='')
    contentType = serializers.CharField(max_length=100, default='')
    content = serializers.CharField(max_length=500, default='')
    author = serializers.CharField(max_length=100, default='')
    categories = serializers.ListField(child=serializers.CharField())
    count = serializers.IntegerField(default=1023)
    comments = serializers.CharField(max_length=100, default='')
    commentsSrc = serializers.ListField(child=serializers.CharField())
    published = serializers.DateTimeField()
    visibility = serializers.BooleanField(default=True)
    unlisted = serializers.BooleanField(default=False)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.title = validated_data.get('title', instance.title)
        instance.id = validated_data.get('id', instance.id)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.description = validated_data.get('description', instance.description)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.count = validated_data.get('count', instance.count)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.commentsSrc = validated_data.get('commentsSrc', instance.commentsSrc)
        instance.published = validated_data.get('published', instance.published)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        return instance
    
    class Meta:
        model = PostsModel
        # Tuple of serialized model fields (see link [2])
        fields = ('type', 'title', 'id', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'comments', 'commentsSrc', 'published', 'visibility', 'unlisted')
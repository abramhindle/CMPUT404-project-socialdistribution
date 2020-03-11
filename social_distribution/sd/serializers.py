
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Author, Post, Comment, FriendRequest, Follow, FriendList


class CreateAuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email', 'uuid']
        # write_only_fields = ('password', 'github')
        read_only_fields = ('uuid',)

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    # def update(self, instance, validated_data):


class LoginAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class GetAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'link_to_image', 'author']
        # fields = '__all__'
        # read_only_fields = ['author']
        # write_only_fields = ['author_id']


class GetPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'link_to_image', 'author', 'uuid']


class DeletePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post

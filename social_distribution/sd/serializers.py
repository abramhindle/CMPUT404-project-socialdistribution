
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Author, Post, Comment, FriendRequest, Follow, Friend


class CreateAuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name',
                  'username', 'password', 'email', 'uuid']
        write_only_fields = ('password')
        # read_only_fields = ('uuid',)

    def create(self, validated_data):
        author = super(CreateAuthorSerializer, self).create(validated_data)
        author.set_password(validated_data['password'])
        author.save()
        return author

    # def update(self, instance, validated_data):


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'link_to_image', 'author', 'uuid']
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)

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


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['author', 'body', 'post']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['author', 'body', 'post']


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ['uuid', 'to_author', 'from_author']

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Post, AuthorProfile, Category


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        None,
                                        validated_data['password'])
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            "Unable to log in with provided credentials.")


class AuthorProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('custom_id')
    url = serializers.SerializerMethodField('custom_id')

    def custom_id(self, obj):
        host = obj.host
        if(obj.host[-1] != "/"):
            host += "/"
        new_id = "{}author/{}".format(host, obj.id)
        return new_id

    class Meta:
        model = AuthorProfile
        fields = (
            'id',
            'host',
            'displayName',
            'url',
            'github',
            'firstName',
            'lastName',
            'email',
            'bio',
            'isValid',
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class PostSerializer(serializers.ModelSerializer):
    author = AuthorProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'title',
            'source',
            'origin',
            'description',
            'contentType',
            'content',
            'author',
            'categories',
            'published',
            'id',
            'visibility',
            'visibleTo',
            'unlisted'
        )

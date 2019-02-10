from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import DummyPost, Post, AuthorProfile


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class DummyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyPost
        fields = ('id', 'text',)

class AuthorProfileSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        # model = AuthorProfile
        # fields =(
        #     'github',

        # )
        
        model = AuthorProfile
        fields= (
            'github',
            'author'
            )

        #def validate(self, data):
            

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )
    #author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'author'
        )

    # def validate(self, data):
    #     print("this is my validation")
    #     print(data)
    #     print(self.context['request'])
    #     if True:
    #         return data
    #     raise serializers.ValidationError("my PostSerializer validate error")

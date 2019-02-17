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


class AuthorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    url = serializers.SerializerMethodField("custom_get_url")
    id = serializers.SerializerMethodField("custom_get_url")

    class Meta:
        model = AuthorProfile
        fields = (
            "id",
            "host",
            "displayName",
            "github",
            "bio",
            "user",
            "firstName",
            "lastName",
            "email"
        )

    def custom_get_url(self, obj):
        host = obj.host
        if(host != "/"):
            host += "/"
        return "{}author/{}".format(host, str(obj.id))


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'author'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
        )

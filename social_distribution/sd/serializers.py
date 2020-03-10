
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

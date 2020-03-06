
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Author, Post, Comment, FriendRequest, Follow, FriendList


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'username', 'password',
                  'first_name', 'last_name', 'email', 'github', 'bio', 'host')
        write_only_fields = ('password', 'github')
        read_only_fields = ('uuid')

        def create(self, validated_data):
            user = super(CreateUserSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user

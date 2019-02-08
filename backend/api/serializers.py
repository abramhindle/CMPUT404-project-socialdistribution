from rest_framework import serializers
from django.contrib.auth.models import User

from .models import DummyPost


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


class DummyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyPost
        fields = ('id', 'text',)

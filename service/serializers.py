# Serializers define the API representation.
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import Field

from dashboard.models import Author
from service.models import FriendRequestAuthor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined',)
        read_only_fields = ('date_joined',)


class AuthorSerializer(serializers.ModelSerializer):
    github = serializers.URLField()
    host = serializers.URLField()
    url = serializers.URLField()


class FriendRequestAuthorSerializer(serializers.ModelSerializer):
    id = serializers.URLField(source='get_id_url', required=True)

    class Meta:
        model = Author

    def create(self, validated_data):
        return FriendRequestAuthor(**validated_data)

    host = serializers.URLField(required=True)
    displayName = serializers.CharField(required=True)
    url = serializers.URLField(required=True)


class FriendRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    author = FriendRequestAuthorSerializer(required=True)
    friend = FriendRequestAuthorSerializer(required=True)

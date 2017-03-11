# Serializers define the API representation.
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import Field

from dashboard.models import Author


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined',)
        read_only_fields = ('date_joined',)


class AuthorSerializer(serializers.ModelSerializer):
    github = serializers.URLField()
    host = serializers.URLField()
    url = serializers.URLField()

    class Meta:
        model = Author
        fields = ('user', 'id', 'displayName', 'github', 'bio', 'activated', 'host', 'url',)

from django.db import models
from .models import Author, Follow, Inbox
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_url", read_only=True)
    url = serializers.CharField(source="get_url", read_only=True)
    type = serializers.CharField(default="author", read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'displayName', 'host', 'type', 'url']
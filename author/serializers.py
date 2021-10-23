from django.db import models
from .models import Author, Follow, Inbox
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    '''
    This serializer is used for GET requests
    '''
    type = serializers.CharField(default="author", read_only=True)
    id = serializers.CharField(source="get_url")
    url = serializers.CharField(source="get_url", read_only=True)

    class Meta:
        model = Author
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage']

    def create(self, validated_data):
        author =  Author(**validated_data, authorID=self.context.get("authorID"))
        author.save()
        return author

    def update(self, instance, validated_data):
        instance.displayName = validated_data.get("displayName", instance.displayName)
        instance.host = validated_data.get("host", instance.host)
        instance.github = validated_data.get("github", instance.github)
        instance.profileImage = validated_data.get("profileImage", instance.profileImage)
        instance.save()
        return instance

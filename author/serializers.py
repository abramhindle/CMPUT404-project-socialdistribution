from django.db import models
from .models import Author, Follow, Inbox
from rest_framework import serializers
from server.models import Node

class AuthorSerializer(serializers.ModelSerializer):
    '''
    This serializer is used for GET requests
    '''
    type = serializers.CharField(default="author", read_only=True)
    id = serializers.CharField(source="get_url")
    url = serializers.CharField(source="get_url", read_only=True)
    host = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Author
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage']

    def create(self, validated_data):
        displayName = validated_data.get("displayName")
        if "host" in validated_data:
            if validated_data.get("host") is not None and validated_data.get("host") != "":
                host = validated_data.get("host")
            else:
                host = validated_data.get("get_url").split("/")[:-2]
        else:
            host = validated_data.get("get_url").split("/")[:-2]
        github = validated_data.get("github")
        profileImage = validated_data.get("profileImage")
        authorID = validated_data.get("get_url").split("/")[-1]
        node = Node.objects.filter(host_url__startswith=host).first()
        author, _ = Author.objects.update_or_create(authorID=authorID, defaults={"displayName": displayName, "host": host, "github": github, "profileImage": profileImage, "node": node})
        #author = Author(authorID=authorID, displayName=displayName, host=host, github=github, profileImage=profileImage, node=self.context.get("node", None))
        author.save()
        return author

    def update(self, instance, validated_data):
        instance.displayName = validated_data.get("displayName", instance.displayName)
        instance.host = validated_data.get("host", instance.host)
        instance.github = validated_data.get("github", instance.github)
        instance.profileImage = validated_data.get("profileImage", instance.profileImage)
        instance.save()
        return instance

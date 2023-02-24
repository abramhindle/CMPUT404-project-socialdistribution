#from django.contrib.auth.models import User, Group
from .models import AuthorModel
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=100, default='')
    id = serializers.CharField(max_length=150, default='')
    url = serializers.CharField(max_length=100, default='')
    host = serializers.CharField(max_length=150,default='')
    displayName = serializers.CharField(max_length=150, default='')
    github = serializers.CharField(max_length=150, default='')
    profileImage = serializers.CharField(max_length=500, default='')

    #TODO: create a method to create a new author
    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.id = validated_data.get('id', instance.id)
        instance.url = validated_data.get('url', instance.url)
        instance.host = validated_data.get('host', instance.host)
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)

        return instance

    class Meta:
        model = AuthorModel
        # Tuple of serialized model fields (see link [2])
        fields = ('type', 'id', 'host', 'displayName', 'github', 'url', 'profileImage')
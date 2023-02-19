from django.contrib.auth.models import User, Group
from .models import AuthorModel
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=100, default='')
    id = serializers.CharField(max_length=150, default='')
    host = serializers.CharField(max_length=150,default='')
    displayName = serializers.CharField(max_length=150, default='')
    github = serializers.CharField(max_length=150, default='')
    url = serializers.CharField(max_length=100, default='')
    profileImageURL = serializers.CharField(max_length=500, default='')

    # TODO: Add update function for author view POST request

    class Meta:
        model = AuthorModel
        # Tuple of serialized model fields (see link [2])
        fields = ('type', 'id', 'host', 'displayName', 'github', 'url', 'profileImageURL')
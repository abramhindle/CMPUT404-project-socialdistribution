from django.contrib.auth.models import User, Group
from .models import AuthorModel
from rest_framework import serializers
import uuid

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=100, blank=False, default='')
    id = serializers.CharField(max_length=150, blank=False, default='')
    host = serializers.CharField(max_length=150, blank=False, default='')
    displayName = serializers.CharField(max_length=150, blank=False, default='')
    github = serializers.CharField(max_length=150, blank=False, default='')
    url = serializers.CharField(max_length=100, blank=False, default='')
    profileImageURL = serializers.CharField(max_length=500, blank=False, default='')

    
    
    def create(self, validated_data):
        validated_data['type']= 'author'
        validated_data['id'] = str(uuid.uuid4())
        validated_data['host'] = 'http://127.0.0.1:5454/authors/' + str(validated_data['id'])
        validated_data['displayName'] = 
        validated_data['host'] = 'http://127.0.0.1:5454/authors/' + str(validated_data['id'])
        validated_data['host'] = 'http://127.0.0.1:5454/authors/' + str(validated_data['id'])
        return AuthorModel.objects.create(**validated_data)

    class Meta:
        model = AuthorModel
        # Tuple of serialized model fields (see link [2])
        
        fields = ( "id", "username", "password", )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
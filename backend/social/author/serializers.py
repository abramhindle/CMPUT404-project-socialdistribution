import uuid
from django.urls import reverse
from rest_framework import serializers, exceptions
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    displayName = serializers.CharField(default = 'x')
    
    @staticmethod
    def extract_and_upcreate_author(validated_data, author_id=None):
        validated_author_data = validated_data.pop('author') if validated_data.get('author') else None
        try:
            if validated_author_data:
                print("if case")
                updated_author = AuthorSerializer._upcreate(validated_author_data)
            else:
                print("else case")
                updated_author = Author.objects.get(id=author_id)
            return updated_author
        except:
            raise exceptions.ValidationError("Author does not exist")
    
    def to_representation(self, instance):
        id = instance.get_public_id()
        id = id[:-1] if id.endswith('/') else id
        return {
            **super().to_representation(instance),
            'id': id
        }
        
    class Meta:
        model = Author
        fields = [
            'type', 
            'id', 
            #'host',
            'displayName',
            'url',
            #'github',
            'profileImage',
        ]
        
class InboxSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    object = serializers.JSONField()

    def get_author(self, data):
        author = self.context.get('author')
        validated_data = {
            'author': author,
            'object': data
        }
        return validated_data

    def to_representation(self, instance):
        return instance.object

    def create(self, validated_data):
        return Inbox.objects.create(**validated_data)
    
    class Meta:
        model = Inbox
        fields = ['author', 'object']
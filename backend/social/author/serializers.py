import uuid
from django.urls import reverse
from rest_framework import serializers, exceptions
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    displayName = serializers.CharField(default = 'x')
    
    @staticmethod
    def _upcreate(validated_data):
        author = Author.objects.create(**validated_data)   
        return author
    @staticmethod
    def extract_and_upcreate_author(validated_data, author_id=None):
        validated_author_data = validated_data.pop('author') if validated_data.get('author') else None
        print("validated",validated_author_data)
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
            #'url',
            #'github',
            'profileImage',
        ]

class FollowRequestSerializer(serializers.ModelSerializer):
    #to_user = serializers.CharField(default = 'x')
    
    actor = AuthorSerializer()
    object = AuthorSerializer()

    class Meta:
        model = FollowRequest
        fields = ['Type','Summary','actor', 'object']
        
class InboxSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="inbox",source="get_api_type",read_only=True)
    # author = serializers.CharField(source="get_author")
    # items = serializers.SerializerMethodField()
    
    def to_representation(self, instance):
        serializer = self.context["serializer"]
        rep = super().to_representation(instance)
        print("HERE MF",serializer(instance))
        rep['content_object'] = serializer(instance)
        return rep

    # def get_items(self, validated_data):
    #     print("INSTANCES",validated_data)
    #     serialize = self.context["serializer"]
    #     s = serialize(validated_data["objects"])
    #     print("Instance is here", s)
    #     return [s]
    
    # def create(self, data):
    #     print("Creating...")
    #     author = self.context["author"]
    #     validated_data = {
    #         'author': author,
    #         'object': data
    #     }
    #     print("OBJECTS create here")
    #     self.get_items(validated_data)
    
    class Meta:
        model = Inbox
        fields = ['type','author', 'content_type', 'object_id' ,'content_object']
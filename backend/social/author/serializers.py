import uuid
from django.urls import reverse
from rest_framework import serializers, exceptions
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    @staticmethod
    def extract_and_upcreate_author(validated_data, author_id=None):
        """
        extract 'author' field from validated_data, and
        - upcreate the author, OR
        - get the author and do nothing if only author_id is given
        raise error if author doesn't exist by author_id AND no data is given
        """
        validated_author_data = validated_data.pop('author') if validated_data.get('author') else None
        try:
            if validated_author_data:
                updated_author = AuthorSerializer._upcreate(validated_author_data)
            else:
                print("else CASE")
                updated_author = Author.objects.get(id=author_id)
            return updated_author
        except:
            raise exceptions.ValidationError("author does not exist for the post")
    
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
        
class AuthorSerializerr(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    displayName = serializers.CharField(default = 'x')
    @staticmethod
    def extract_and_upcreate_author(validated_data, author_id=None):
        """
        extract 'author' field from validated_data, and
        - upcreate the author, OR
        - get the author and do nothing if only author_id is given
        raise error if author doesn't exist by author_id AND no data is given
        """
        validated_author_data = validated_data.pop('author') if validated_data.get('author') else None
        try:
            if validated_author_data:
                updated_author = AuthorSerializer._upcreate(validated_author_data)
            else:
                print("else CASE")
                updated_author = Author.objects.get(id=author_id)
            return updated_author
        except:
            raise exceptions.ValidationError("author does not exist for the post")
  
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
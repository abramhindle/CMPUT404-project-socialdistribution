from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    class Meta:
        model = Author
        
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
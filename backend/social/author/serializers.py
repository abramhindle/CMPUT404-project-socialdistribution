from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    
    @staticmethod
    def _update(instance, validated_data):
        """
        method used to modify model, if serializer is used as `partial=True`
        use static method to avoid creating a serializer when data is already valid,
        which happens often in other objects like Post, Like where Author is nested inside.
        """
        instance.display_name = validated_data.get(
            'display_name', instance.display_name)
        instance.save()
        return instance
    
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
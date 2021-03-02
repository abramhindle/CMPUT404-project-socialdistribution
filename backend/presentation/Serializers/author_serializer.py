from rest_framework import serializers
from presentation.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['_type', 'id', 'host', 'displayName', 'url', 'github']

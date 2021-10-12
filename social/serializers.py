from rest_framework import serializers

from .models import Author

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'display_name', 'url', 'github')
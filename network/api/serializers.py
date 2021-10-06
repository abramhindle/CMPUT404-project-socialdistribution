from rest_framework import serializers
from network.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['task','completed','timestamp','updated','user']

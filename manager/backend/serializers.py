from rest_framework import serializers
from backend.models import Author

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField('get_type')
    id = serializers.SerializerMethodField('set_id')

    def get_type(self, Author):
      return "author" 

    def set_id(self, Author):
        return str(Author.host)+"/"+str(Author.id)

    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'displayName', 'url', 'github')

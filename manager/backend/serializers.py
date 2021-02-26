from rest_framework import serializers
from .models import Author, Post

# Author Serializer


class AuthorSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField('get_type')
    id = serializers.SerializerMethodField('set_id')

    def get_type(self, Author):
    	return "author"

    def set_id(self, Author):
        return str(Author.host)+"/author/"+str(Author.id)+'/'

    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'displayName', 'url', 'github')

class PostSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = "__all__"


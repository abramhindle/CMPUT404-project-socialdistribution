from rest_framework import serializers
from .models import Author, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])

    return user
class PostSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = "__all__"


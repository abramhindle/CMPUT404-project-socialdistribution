from rest_framework import serializers
from .models import Author, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# User Serializer
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


class CreateAuthorSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField('get_type')
    author_id = serializers.SerializerMethodField('set_id')
    token = serializers.SerializerMethodField('set_token')

    def __init__(self, *args, **kwargs):
        print(args)
        Author.token = args[0]

    def get_type(self, Author):
    	return "author"

    def set_id(self, Author):
        return str(Author.host)+"/author/"+str(Author.author_id)+'/'
    
    def set_token(self, Author):
        return str(Author.token)

    def create(self, validated_data):
        return Author()

    class Meta:
        model = Author
        fields = ('token', 'author_id', 'host', 'displayName', 'url', 'github')

    




class AuthorSerializer(serializers.ModelSerializer):

    type = serializers.SerializerMethodField('get_type')
    id = serializers.SerializerMethodField('set_id')

    def get_type(self, Author):
    	return "author"

    def set_id(self, Author):
        return str(Author.host)+"/author/"+str(Author.author_id)+'/'

    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'displayName', 'url', 'github')




class PostSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = "__all__"


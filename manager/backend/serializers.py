from rest_framework import serializers
from backend.models import Author
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
    fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

    return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect Credentials")
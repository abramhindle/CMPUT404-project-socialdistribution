from rest_framework import serializers
from .models import Author, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# User Serializer
class UserSerializer(serializers.ModelSerializer):
	"""
	This class serializes User data to output an 'id' and 'username'.
	"""
	class Meta:
		model = User
		fields = ('id', 'username')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
	"""
	This class serializes Registration data to output 'id', 'username' and 'password'.
	"""
	class Meta:
		model = User
		fields = ('id', 'username', 'password')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		"""
		The 'create' method is run when a new User is created
		"""
		return User.objects.create_user(username=validated_data['username'], password=validated_data['password'])

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
	"""
	This class serializes Author data to output all of the field names for the Author object.
	"""

	type = serializers.SerializerMethodField('get_type')
	id = serializers.SerializerMethodField('set_id')

	def get_type(self, Author):
		"""
		The get_type method is run every time serialization occurs and returns the appropriate string for the JSON 'type' field.
		"""
		return "author"

	def set_id(self, Author):
		"""
		The set_id method is run every time serialization occurs and returns the 'id' field as the proper url format. This is because ids are stored as just the uuid vlaue in the DB,
		but the API requires the uuid be returned as a url
		"""
		return str(Author.host)+"author/"+str(Author.id)+'/'

	class Meta:
		model = Author
		fields = ('type', 'id', 'host', 'displayName', 'url', 'github')



# Post Serializer
class PostSerializer(serializers.ModelSerializer):
	"""
	This class serializes Post data to output all of the field names for the Post object.
	"""

	type = serializers.SerializerMethodField('get_type')

	def get_type(self, Post):
		"""
		The get_type method is run every time serialization occurs and returns the appropriate string for the JSON 'type' field.
		"""
		return "post"

	class Meta:
		model = Post
		fields = ('type', 'title', 'id', 'source', 'origin', 'description', 'content_type', 'content', 'categories', 'count', 'published', 'visibility', 'unlisted', 'author_id')


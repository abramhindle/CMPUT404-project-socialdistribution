from rest_framework import serializers
from .models import Author, Post, Comment, Like
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from urllib import request



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
		return "http://" + str(Author.host)+"/author/"+str(Author.id)

	class Meta:
		model = Author
		fields = ('type', 'id', 'host', 'displayName', 'url', 'github')


class CommentSerializer(serializers.ModelSerializer):
	"""
	This class serializes the Comment data to ouput the neccessary fields from the table.
	"""
	author = AuthorSerializer()
	type = serializers.SerializerMethodField('get_type')
	id = serializers.SerializerMethodField('get_id')

	def get_type(self, Comment):
		"""
		The get_type method is run every time serialization occurs and returns the appropriate string for the JSON 'type' field.
		"""
		return "comment"

	def get_id(self, Comment):
		"""
		The get_id method is run every time serialization occurs and returns the 'id' field as the proper url format. This is because ids are stored as just the uuid vlaue in the DB,
		but the API requires the uuid be returned as a url
		"""
		return "http://" + str(Comment.host) + "/author/" + str(Comment.post_author_id) + "/posts/" + str(Comment.post.id) + "/comments/" + str(Comment.id)

	class Meta:
		model = Comment
		fields = ('type', 'author', 'comment', 'contentType', 'published', 'id')
		depth = 1

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
	"""
	This class serializes Post data to output all of the field names for the Post object.
	"""
	author = AuthorSerializer()
	type = serializers.SerializerMethodField('get_type')
	id = serializers.SerializerMethodField('get_id')
	comments = CommentSerializer(many=True)
	commentLink = serializers.SerializerMethodField('get_comment_link')

	def get_type(self, Post):
		"""
		The get_type method is run every time serialization occurs and returns the appropriate string for the JSON 'type' field.
		"""
		return "post"

	def get_id(self, Post):
		"""
		The get_id method is run every time serialization occurs and returns the 'id' field as the proper url format. This is because ids are stored as just the uuid vlaue in the DB,
		but the API requires the uuid be returned as a url
		"""
		return "http://" + str(Post.host) + "/author/" + str(Post.author_id) + "/posts/" + str(Post.id)

	def get_comment_link(self, Post):
		return  "http://" + str(Post.host) + "/author/" + str(Post.author_id) + "/posts/" + str(Post.id) + "/comments"

	class Meta:
		model = Post
		fields = ('type', 'title', 'id', 'source', 'origin', 'description', 'content_type', 'content', 'categories', 'count', 'commentLink', 'comments', 'published', 'visibility', 'unlisted', 'author')
		depth = 1


class LikeSerializer(serializers.ModelSerializer):
	"""
	This class serializes the Like data to ouput the neccessary fields from the table.
	"""

	author = AuthorSerializer()
	type = serializers.SerializerMethodField('get_type')
	context = serializers.SerializerMethodField('get_context')
	object = serializers.SerializerMethodField('get_object')

	def get_type(self, Like):
		"""
		The get_type method is run every time serialization occurs and returns the appropriate string for the JSON 'type' field.
		"""
		return "like"

	def get_context(self, Like):
		"""
		The get_context method is run every time serialization occurs and returns the appropriate string for the JSON 'context' field.
		"""
		return "https://www.w3.org/ns/activitystreams"


	def get_object(self, Like):
		if Like.comment:
			return "https://"+self.context['request'].META['HTTP_HOST']+"/author/" + Like.post.author.id + "/posts/" + Like.post.id + "/comments/" + Like.comment.id
		else:
			return "https://"+self.context['request'].META['HTTP_HOST']+"/author/" + Like.post.author.id + "/posts/" + Like.post.id

	class Meta:
		model = Like
		fields = ('context','summary', 'type', 'author', 'object')
		depth = 1

	def to_representation(self, instance):
		data = super().to_representation(instance)
		data.update({"@context":data["context"]})
		data.move_to_end('@context', last=False)
		del data["context"]
		return data

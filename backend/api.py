from django.db.models import query
from django.http import request
from .models import Author, Inbox, Post, Comment, Like, Follow
from rest_framework import serializers, viewsets, permissions, generics, status, filters
from rest_framework.response import Response
from .serializers import AuthorSerializer, CommentSerializer, FollowSerializer, LikeSerializer, RegisterSerializer, UserSerializer, PostSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
import json

class RegisterAPI(generics.GenericAPIView):
	"""
	This class provides an API for user and author registration.
	"""

	serializer_class = RegisterSerializer

	def post(self, request, *args, **kwargs):
		"""
		This method provides POST functionality to creating a user and author, by serializing a user object that is created into the Django authentication system, then creating a POST request with the author data.
		"""
		# Get and serialize the request data
		serializer = self.get_serializer(data=request.data)

		# Check the validity
		serializer.is_valid(raise_exception=True)

		# Create the user
		user = serializer.save()
		# Create an authentication token for the provided user
		token = Token.objects.create(user=user)

		# Create the author object
		author = Author(
						token=token,
						user=user,
						displayName=request.data["displayName"],
						github=request.data["github"],
						host = request.META['HTTP_HOST'],
						)

		# Save the author information into the database
		author.url = "http://"+str(author.host)+"/author/"+str(author.id)
		author.save()
		# Serialize the author data for a POST response
		authorData = AuthorSerializer(author, context=self.get_serializer_context()).data

		return Response(authorData)

class UserAPI(generics.RetrieveAPIView):

	permission_classes = [
		permissions.IsAuthenticated,
	]

	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user

class AuthorViewSet(viewsets.ModelViewSet):
	"""
	This class specifies the view for the Post objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""
	# Specifies the query set on which this view can act
	queryset = Author.objects.all()

	# Specifies the permissions needed to access and modify the data
	permission_classes = [
		permissions.IsAuthenticated
	]

	# Specifies the serializer used to return the correctly formatted JSON response body
	serializer_class = AuthorSerializer

	# Specifies the lookup field to use the in the database
	lookup_field = 'id'

	def update(self, request, *args, **kwargs):
		"""
		This method will be called when a POST request is received for a specific author.
		"""

		# Code to extract specifically the author's id value from the url in the JSON request's id field
		author_id = request.data["id"]
		newID = author_id.split("/")[-2]

		# Update the request object's data so the id field is correctly formatted to be found in the DB
		request.data.update({"id": newID})

		return super().update(request, *args, **kwargs)

class LoginAPI(viewsets.ModelViewSet):

	queryset = Author.objects.all()

	permission_classes = [
		permissions.AllowAny
	#	permissions.IsAuthenticated
	]

	lookup_field = 'id'


	serializer_class = AuthorSerializer

	def update(self, request, *args, **kwargs):

		queryset = Author.objects.all()

		body = json.loads(request.body)
		username = body['username']
		password = body['password']

		user = authenticate(request, username=username, password = password)

		if user is not None:
			login(request, user)

			query_author = queryset.filter(user=user).get()
			serializer = self.get_serializer(query_author)

			return Response(serializer.data)

		else:
			print('Login error')
			return Response(status=status.HTTP_404_NOT_FOUND)

class PostViewSet(viewsets.ModelViewSet):
	"""
	This class specifies the view for the Post objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.AllowAny
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = PostSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Post.objects.all()

	def list(self, request, author_id=None, id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint. This will retrieved the user's post list and return the response.
		"""
		if author_id:
			# Filter post table on the author_id in the url and order the results by the most recent at the top
			posts = Post.objects.filter(id=author_id).order_by('-published')

			# Get the serializer and serialize the returned post table rows
			serializer = self.get_serializer(posts, many=True)

			# Return the serializer output data as the response
			return Response(serializer.data)
		return super().list(request, *args, **kwargs)

	def retrieve(self, request, author_id=None, id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint with a specific id for the post. This will retrieved the post's information and return the response.
		"""
		if author_id and id:
			# Filter the post table on the id of the post in the url
			post = Post.objects.filter(id=id).get()

			# Get the serializer and serialize the returned post table rows
			serializer = self.get_serializer(post)

			# Return the serializer output data as the response
			return Response(serializer.data)
		return super().retrieve(request, *args, **kwargs)

	def destroy(self, request, author_id=None, id=None, *args, **kwargs):
		"""
		This method is run in the case that a DELETE request is retrieved by the API for the post endpoint. This will delete the post from the Post table.
		"""
		if author_id and id:
			# Filter the post table on the id of the post in the url
			post = Post.objects.filter(id=id)

			# Get the serializer and serialize the returned post table rows
			serializer = self.get_serializer(post, many=True)

			# Stores the post before it is deleted so that it can be sent back to the user
			deleted_post = serializer.data

			# Delete the post from the DB
			post.delete()

			# Return the serializer output data as the response
			return Response(deleted_post)
		return super().destroy(request, *args, **kwargs)

	def create(self, request, author_id=None, id=None, *args, **kwargs):
		if author_id and id:
			if request.data["contentType"] in ['application/base64', 'image/png', 'image/jpeg']:
				post = Post(
					author = Author.objects.filter(id=author_id).get(),
					id = id,
					title = request.data["title"],
					source = request.data["source"],
					origin = request.data["origin"],
					host = self.request.META['HTTP_HOST'],
					description = request.data["description"],
					content_type = request.data["contentType"],
					image_content = request.data["content"],
					categories = request.data["categories"],
					visibility = request.data["visibility"],
					unlisted = request.data["unlisted"]
				)
			else:
				post = Post(
					author = Author.objects.filter(id=author_id).get(),
					id = id,
					title = request.data["title"],
					source = request.data["source"],
					origin = request.data["origin"],
					host = self.request.META['HTTP_HOST'],
					description = request.data["description"],
					content_type = request.data["contentType"],
					content = request.data["content"],
					categories = request.data["categories"],
					visibility = request.data["visibility"],
					unlisted = request.data["unlisted"]
				)
		elif author_id:
			if request.data["contentType"] in ['application/base64', 'image/png', 'image/jpeg']:
				post = Post(
					author = Author.objects.filter(id=author_id).get(),
					title = request.data["title"],
					source = request.data["source"],
					origin = request.data["origin"],
					host = self.request.META['HTTP_HOST'],
					description = request.data["description"],
					content_type = request.data["contentType"],
					image_content = request.data["content"],
					categories = request.data["categories"],
					visibility = request.data["visibility"],
					unlisted = request.data["unlisted"]
				)
			else:
				post = Post(
					author = Author.objects.filter(id=author_id).get(),
					title = request.data["title"],
					source = request.data["source"],
					origin = request.data["origin"],
					host = self.request.META['HTTP_HOST'],
					description = request.data["description"],
					content_type = request.data["contentType"],
					content = request.data["content"],
					categories = request.data["categories"],
					visibility = request.data["visibility"],
					unlisted = request.data["unlisted"]
				)
		post.save()
		if post.visibility == 'FRIENDS':
			followers = Follow.objects.filter(followee=post.author.id, friends=True)
			for follower in followers.iterator():
				#follower_author = Author.objects.filter(id=follower.follower).get()
				inbox = Inbox(
					author = follower.follower,
					post = post
				)
				inbox.save()
		elif post.visibility == 'PUBLIC':
			followers = Follow.objects.filter(followee=post.author.id)
			for follower in followers.iterator():
				#follower_author = Author.objects.filter(id=follower.follower).get()
				inbox = Inbox(
					author = follower.follower,
					post = post
				)
				inbox.save()

		serializer = self.get_serializer(post)
		#serializer = CommentSerializer(data=self.get_serializer(comment).data)
		#serializer.is_valid(raise_exception=True)
		#serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
	"""
	This class specifies the view for the Comment objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""

	permission_classes = [
		permissions.AllowAny
	]

	lookup_field = 'post'

	serializer_class = CommentSerializer

	queryset = Comment.objects.all()

	def create(self, request, author_id=None, post_id=None, *args, **kwargs):

		comment = Comment(
			author = Author.objects.filter(id=author_id).get(),
			post = Post.objects.filter(id=post_id).get(),
			comment = request.data["comment"],
			contentType = request.data["contentType"],
			host = self.request.META['HTTP_HOST'],
			post_author_id = author_id
		)
		comment.save()
		serializer = self.get_serializer(comment)
		#serializer = CommentSerializer(data=self.get_serializer(comment).data)
		#serializer.is_valid(raise_exception=True)
		#serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class LikeAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the Like objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.AllowAny
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = LikeSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Like.objects.all()


	def list(self, request, author_id=None, post_id=None, comment_id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint. This will retrieved the user's post list and return the response.
		"""
		if request.user.is_authenticated:

			user_author = Author.objects.filter(user=request.user.id).get()

			if user_author.id == author_id:

				if comment_id:
					likes = Like.objects.filter(post=post_id, comment=comment_id)
					serializer = self.get_serializer(likes, many=True)

					return Response(serializer.data)
				else:
					likes = Like.objects.filter(post=post_id)
					serializer = self.get_serializer(likes, many=True)

					return Response(serializer.data)

		return Response(status=status.HTTP_403_FORBIDDEN)


	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['displayName'] = Author.objects.filter(user=self.request.user.id).get().displayName
		return context

class NameAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the displayName objects. This will run methods to retrieve DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.IsAuthenticated
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = AuthorSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Author.objects.all()

	def list(self, request, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint. This will retrieved the user's post list and return the response.
		"""

		if request.user.is_authenticated:

			if request.query_params.get('more'):
				authors = Author.objects.filter(displayName__icontains=request.data['displayName'])
			else:
				authors = Author.objects.filter(displayName__icontains=request.data['displayName'])[:5]

			serializer = self.get_serializer(authors, many=True)

			return Response(serializer.data)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

class LikedAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the a list of Likes by an Author. This will run methods to retrieve DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.AllowAny
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = LikeSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Like.objects.all()


	def list(self, request, author_id=None, post_id=None, comment_id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint. This will retrieved the user's post list and return the response.
		"""

		if request.user.is_authenticated:

			likes = Like.objects.filter(author=author_id, post__visibility="PUBLIC")
			serializer = self.get_serializer(likes, many=True)


			return Response({
				"type":"liked",
				"items": serializer.data
			})

		return Response(status=status.HTTP_403_FORBIDDEN)


	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['displayName'] = Author.objects.filter(user=self.request.user.id).get().displayName
		return context

class InboxAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the a list of Likes by an Author. This will run methods to retrieve DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.IsAuthenticated
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = FollowSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Inbox.objects.all()

	def list(self, request, author_id=None, *args, **kwargs):

		if author_id:

			follows_list = Inbox.objects.filter(author=author_id, follow__isnull=False)
			posts_list = Inbox.objects.filter(author=author_id, post__isnull=False)
			likes_list = Inbox.objects.filter(author=author_id, like__isnull=False)

			follows = Follow.objects.filter(follow__in=follows_list)
			posts = Post.objects.filter(post__in=posts_list)
			likes = Like.objects.filter(like__in=likes_list)

			post_serializer = PostSerializer(posts, many=True)
			follow_serializer = FollowSerializer(follows, many=True)
			like_serializer = LikeSerializer(likes, many=True, context={'request': request})

			return Response({
				"type":"inbox",
				"author":"http://"+self.request.META['HTTP_HOST']+"/author/"+author_id,
				"items": follow_serializer.data+like_serializer.data+post_serializer.data
			})
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def create(self, request, author_id=None, *args, **kwargs):

		if author_id:

			if request.data['type'] == 'Follow':

				actor_id = request.data['actor']['id'].split("/")[-1]
				object_id = request.data['object']['id'].split("/")[-1]

				actor = Author.objects.filter(id=actor_id).get()
				object = Author.objects.filter(id=object_id).get()

				check_follow = Follow.objects.filter(follower=object, followee=actor)

				if object_id == author_id:
					if check_follow:
						follow = Follow(
							follower=actor,
							followee=object,
							friends = True,
							summary=actor.displayName + " wants to follow " + object.displayName
						)
						check_follow.update(friends=True)

					else:
						follow = Follow(
							follower=actor,
							followee=object,
							summary=actor.displayName + " wants to follow " + object.displayName
						)
					follow.save()
					serializer = self.get_serializer(follow)

					inbox = Inbox(
						author=object,
						follow=follow
					)
					inbox.save()
					return Response(serializer.data, status=status.HTTP_201_CREATED)

			elif request.data['type'] == 'Like':

				check_id = request.data['object'].split('/')[-1]
				check_type = request.data['object'].split('/')[-2]
				check_author_id = request.data['object'].split('/')[4]
				like_author_id = request.data['author']['id'].split('/')[-1]
				like_author = Author.objects.filter(id=like_author_id).get()
				check_author = Author.objects.filter(id=check_author_id).get()

				if check_author_id == author_id:
					if check_type == 'posts':

						post=Post.objects.filter(id=check_id).get()

						if not Like.objects.filter(author=like_author, post=post):
							like = Like(
								post=post,
								author=like_author,
								summary=like_author.displayName+" Likes your post"
							)
							like.save()
						else:
							return Response(status=status.HTTP_400_BAD_REQUEST)
					if check_type == 'comments':
						post_id = request.data['object'].split('/')[-3]
						comment = Comment.objects.filter(id=check_id)

						if not Like.objects.filter(author=like_author, comment=comment):
							like = Like(
								post=Post.objects.filter(id=post_id).get(),
								author=like_author,
								comment=comment,
								summary=like_author.displayName+" Likes your comment"
							)
							like.save()
						else:
							return Response(status=status.HTTP_400_BAD_REQUEST)
					serializer = LikeSerializer(like, context={'request': request})
					inbox = Inbox(
						author=check_author,
						like=like
					)
					inbox.save()
					return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(status=status.HTTP_403_FORBIDDEN)


class FollowerAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the a list of Followers for an Author. This will run methods to retrieve DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.IsAuthenticated
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = FollowSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Follow.objects.all()

	def list(self, request, author_id=None, *args, **kwargs):

		if author_id:

			output = []
			follows = Follow.objects.filter(followee=author_id)

			for follow in follows.iterator():
				author = Author.objects.filter(id=follow.follower.id).get()
				serialized = AuthorSerializer(author)
				output.append(serialized.data)

			return Response({
				"type": "followers",
				"items": output
			})
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def destroy(self, request, author_id=None, foreign_id=None, *args, **kwargs):

		if author_id and foreign_id:
			try:
				follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
			except:
				return Response(status.HTTP_404_NOT_FOUND)

			deleted_follow = self.get_serializer(follow)

			if follow:
				follow.delete()

			# Return the serializer output data as the response
			return Response(deleted_follow.data)

		return super().destroy(request, *args, **kwargs)







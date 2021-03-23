from ..models import Author, Follow, Inbox, Post
from ..serializers import PostSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

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
			if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
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
			if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
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
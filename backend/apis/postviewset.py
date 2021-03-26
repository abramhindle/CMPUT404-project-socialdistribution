from ..models import Author, Follow, Inbox, Node, Post
from ..serializers import PostSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
import datetime
import requests

class PostViewSet(viewsets.ModelViewSet):
	"""
	This class specifies the view for the Post objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.IsAuthenticated
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
		# TODO add pagination to retreiving chunks of recent posts
		if request.user.is_authenticated:
			if author_id:
				# Filter post table on the author_id in the url and order the results by the most recent at the top
				posts = Post.objects.filter(author=author_id, visibility="PUBLIC").order_by('-published')

				if not posts:
					return Response(status=status.HTTP_404_NOT_FOUND, data="User has no public posts!")

				# Get the serializer and serialize the returned post table rows
				serializer = self.get_serializer(posts, many=True)

				# Return the serializer output data as the response
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST, data="Unable to parse author id from request")
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def retrieve(self, request, author_id=None, id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint with a specific id for the post. This will retrieved the post's information and return the response.
		"""
		if request.user.is_authenticated:
			if author_id and id:
				# Filter the post table on the id of the post in the url
				try:
					#post = Post.objects.filter(id=id).get()
					post = Post.objects.filter(id=id).get()
				except:
					return Response(status=status.HTTP_404_NOT_FOUND)

				try:
					post = Post.objects.filter(id=id, visibility="PUBLIC").get()
				except:
					return Response(status=status.HTTP_403_FORBIDDEN, data="Post is not public!")

				# Get the serializer and serialize the returned post table rows
				serializer = self.get_serializer(post)

				# Return the serializer output data as the response
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def destroy(self, request, author_id=None, id=None, *args, **kwargs):
		"""
		This method is run in the case that a DELETE request is retrieved by the API for the post endpoint. This will delete the post from the Post table.
		"""
		if request.user.is_authenticated:

			try:
				request_author = Author.objects.filter(user=request.user, id=author_id).get()
			except:
				return Response(status=status.HTTP_403_FORBIDDEN, data="User cannot delete this post!")

			if request_author and id:
				# Filter the post table on the id of the post in the url
				try:
					post = Post.objects.filter(id=id).get()
				except:
					return Response(status=status.HTTP_404_NOT_FOUND)

				# Get the serializer and serialize the returned post table rows
				serializer = self.get_serializer(post)

				# Stores the post before it is deleted so that it can be sent back to the user
				deleted_post = serializer.data

				# Delete the post from the DB
				post.delete()

				# Return the serializer output data as the response
				return Response(deleted_post, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def create(self, request, author_id=None, id=None, *args, **kwargs):

		try:
			author = Author.objects.filter(id=author_id, user=request.user).get()
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if request.user.is_authenticated:

			if author and id:
				if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
					post = Post(
						author = author,
						id = id,
						title = request.data["title"],
						source = request.data["source"],
						origin = request.data["origin"],
						host = self.request.META['HTTP_HOST'],
						description = request.data["description"],
						contentType = request.data["contentType"],
						image_content = request.data["content"],
						categories = request.data["categories"],
						visibility = request.data["visibility"],
						unlisted = request.data["unlisted"]
					)
				else:
					post = Post(
						author = author,
						id = id,
						title = request.data["title"],
						source = request.data["source"],
						origin = request.data["origin"],
						host = self.request.META['HTTP_HOST'],
						description = request.data["description"],
						contentType = request.data["contentType"],
						content = request.data["content"],
						categories = request.data["categories"],
						visibility = request.data["visibility"],
						unlisted = request.data["unlisted"]
					)
			elif author:
				if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
					post = Post(
						author = author,
						title = request.data["title"],
						source = request.data["source"],
						origin = request.data["origin"],
						host = self.request.META['HTTP_HOST'],
						description = request.data["description"],
						contentType = request.data["contentType"],
						image_content = request.data["content"],
						categories = request.data["categories"],
						visibility = request.data["visibility"],
						unlisted = request.data["unlisted"]
					)
				else:
					post = Post(
						author = author,
						title = request.data["title"],
						source = request.data["source"],
						origin = request.data["origin"],
						host = self.request.META['HTTP_HOST'],
						description = request.data["description"],
						contentType = request.data["contentType"],
						content = request.data["content"],
						categories = request.data["categories"],
						visibility = request.data["visibility"],
						unlisted = request.data["unlisted"]
					)
			post.save()
			if post.visibility == 'FRIENDS':
				followers = Follow.objects.filter(followee=post.author.id, friends=True)
				for follower in followers.iterator():


					try:
						follower_author = Author.objects.filter(id=follower.follower).get()
						node = Node.objects.filter(local_username=request.user.username).get()
						s = requests.Session()
						s.auth = (node.remote_username, node.remote_password)
						s.headers.update({'Content-Type':'application/json'})
						response = s.post(node.host+"author/"+follower_author.id+"/inbox/", json=post)
					except Exception as e:
						response = "This didn't work"
						print(e)

					print(response)

					inbox = Inbox(
						author = follower.follower,
						post = post
					)
					inbox.save()
			elif post.visibility == 'PUBLIC':
				followers = Follow.objects.filter(followee=post.author.id)
				for follower in followers.iterator():

					try:
						follower_author = Author.objects.filter(id=follower.follower).get()
						node = Node.objects.filter(local_username=request.user.username).get()
						s = requests.Session()
						s.auth = (node.remote_username, node.remote_password)
						s.headers.update({'Content-Type':'application/json'})
						s.post(node.host+"author/"+follower_author.id+"/inbox/", json=post)
					except Exception as e:
						print(e)

					inbox = Inbox(
						author = follower.follower,
						post = post
					)
					inbox.save()

			serializer = self.get_serializer(post)

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def update(self, request, author_id=None, id=None, *args, **kwargs):

		try:
			post = Post.objects.filter(id=id).get()
		except:
			return Response(status=status.HTTP_404_NOT_FOUND, data="Could not find the post specified!")

		try:
			author = Author.objects.filter(id=author_id, user=request.user).get()
		except:
			return Response(status=status.HTTP_403_FORBIDDEN, data="User cannot modify this post!")

		if author and post:

			post.title = request.data["title"]
			post.source = request.data["source"]
			post.description = request.data["description"]
			post.categories = request.data["categories"]
			post.published = datetime.datetime.now().isoformat()
			post.visibility = request.data["visibility"]
			post.unlisted = request.data["unlisted"]
			post.contentType = request.data["contentType"]

			if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
				post.image_content = request.data["content"]
			else:
				post.content = request.data["content"]

			serializer = self.get_serializer(post)

			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN, data="User cannot modify this post!")
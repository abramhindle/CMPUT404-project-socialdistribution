from manager.settings import HOSTNAME
from ..models import Author, Follow, Inbox, Node, Post
from ..serializers import PostSerializer
from manager.paginate import ResultsPagination

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

	# Set the pagination class for posts
	pagination_class = ResultsPagination

	def list(self, request, author_id=None, id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint. This will retrieve the user's post list and return the response.
		"""
		if request.user.is_authenticated:
			if author_id:
				self.pagination_class = ResultsPagination
				# Filter post table on the author_id in the url and order the results by the most recent at the top
				posts = Post.objects.filter(author=author_id, visibility="PUBLIC").order_by('-published')

				if not posts:
					return Response(status=status.HTTP_404_NOT_FOUND, data="User has no public posts!")

				# Get the serializer and serialize the returned post table rows
				serializer = self.get_serializer(posts, many=True)
				paginated_serializer_data = self.paginate_queryset(serializer.data)
				# Return the serializer output data as the response
				return Response(paginated_serializer_data, status=status.HTTP_200_OK)
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
		"""
		This method will create a new instance of a post, taking in a request body, author ID and a possible post ID argument
		"""
		# Check if the author is valid
		try:
			author = Author.objects.filter(id=author_id, user=request.user).get()
		except:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		already_exists = False
		# Check if the post already exists in the database, if the post exists in our pass over the creation process
		try:
			post = Post.objects.filter(id=id).get()
			already_exists = True
		except:
			pass
		# Verify that the user is authenticated
		if request.user.is_authenticated:
			# If the post does not already exist, create a new post
			if already_exists == False:
				# if an author and ID are passed
				if author and id:
					# For a post with image content
					if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
						post = Post(
							author = author,
							id = id,
							title = request.data["title"],
							host = HOSTNAME,
							description = request.data["description"],
							contentType = request.data["contentType"],
							image_content = request.data["content"],
							categories = request.data["categories"],
							visibility = request.data["visibility"],
							unlisted = request.data["unlisted"]
						)
					# If the post does not contain image content
					else:
						post = Post(
							author = author,
							id = id,
							title = request.data["title"],
							host = HOSTNAME,
							description = request.data["description"],
							contentType = request.data["contentType"],
							content = request.data["content"],
							categories = request.data["categories"],
							visibility = request.data["visibility"],
							unlisted = request.data["unlisted"]
						)
				# If only an author is passed, then create a new post
				elif author:
					# For a post with image content
					if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
						post = Post(
							author = author,
							title = request.data["title"],
							host = HOSTNAME,
							description = request.data["description"],
							contentType = request.data["contentType"],
							image_content = request.data["content"],
							categories = request.data["categories"],
							visibility = request.data["visibility"],
							unlisted = request.data["unlisted"]
						)
					# If the post does not contain image content
					else:
						post = Post(
							author = author,
							title = request.data["title"],
							host = HOSTNAME,
							description = request.data["description"],
							contentType = request.data["contentType"],
							content = request.data["content"],
							categories = request.data["categories"],
							visibility = request.data["visibility"],
							unlisted = request.data["unlisted"]
						)
				# Store the new post object
				post.save()

			serializer = self.get_serializer(post)
			# If the post is set to friends only visibility
			if post.visibility == 'FRIENDS':
				# Get a list of followers for the author posting
				followers = Follow.objects.filter(followee=post.author.id, friends=True)
				# Iterate through all of the author's followers
				for follower in followers.iterator():

					# Try to send the inbox request to the friends inbox, if the authenitcated user is not a node, create the inbox item in the local friends inbox
					try:
						print(follower.follower.user.username)
						# If the friend is a local author, this query will not return any results and will cause an exception that will avoid sending the request and save it the the local inbox
						node = Node.objects.filter(local_username=follower.follower.user.username).get()
						s = requests.Session()
						s.auth = (node.remote_username, node.remote_password)
						s.headers.update({'Content-Type':'application/json'})
						print("POST to:", node.host+"author/"+follower.follower.id+"/inbox", json=serializer.data)
						response = s.post(node.host+"author/"+follower.follower.id+"/inbox", json=serializer.data)
					except:
						# Create the post in the inbox of the friend if the friend is local to the server
						inbox = Inbox(
							author = follower.follower,
							post = post
						)
						inbox.save()
			elif post.visibility == 'PUBLIC': # If the post is public, send it to all the followers of the posts author

				# Retrieve the followers of the post author
				followers = Follow.objects.filter(followee=post.author.id)

				# Loop to run through each follower and try to send the post to their inbox if they are a remote user
				for follower in followers.iterator():

					# Try to send the inbox request to the folllowers inbox
					try:
						# If the follower is a local author, this query will not return any results and will cause an exception that will avoid sending the request
						print(follower.follower.user.username)
						node = Node.objects.filter(local_username=follower.follower.user.username).get()
						s = requests.Session()
						s.auth = (node.remote_username, node.remote_password)
						s.headers.update({'Content-Type':'application/json'})
						print("POST to:", node.host+"author/"+follower.follower.id+"/inbox", json=serializer.data)
						response = s.post(node.host+"author/"+follower.follower.id+"/inbox", json=serializer.data)
					except:
						# Create the post in the inbox of the follower if the follower is local to the server
						inbox = Inbox(
							author = follower.follower,
							post = post
						)
						inbox.save()

			# Return the newly created and serialized post
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			# If the user is not authenticated, return a 403 Forbidden
			return Response(status=status.HTTP_403_FORBIDDEN)

	def update(self, request, author_id=None, id=None, *args, **kwargs):
		"""
		This method will be called when a POST request is received for a specific post to update the information for the post.
		"""

		# Try to get the post object specified in the requests url
		try:
			post = Post.objects.filter(id=id).get()
		except:
			return Response(status=status.HTTP_404_NOT_FOUND, data="Could not find the post specified!")

		# Try to get the author of the post from the database based on the author id in the requests url and the authenticated user who made the request
		try:
			author = Author.objects.filter(id=author_id, user=request.user).get()
		except:
			# If the author could not be found or is not associated with the authenicated user who made the request, send back a 403
			return Response(status=status.HTTP_403_FORBIDDEN, data="User cannot modify this post!")

		if author and post:

			# Edit the information of the post based on the information passed in the requests body
			try:
				post.title = request.data["title"]
				post.source = request.data["source"]
				post.description = request.data["description"]
				post.categories = request.data["categories"]
				post.published = datetime.datetime.now().isoformat()
				post.visibility = request.data["visibility"]
				post.unlisted = request.data["unlisted"]
				post.contentType = request.data["contentType"]

				# Check the type of content being sent in the post and store it in the correct place
				if any([types in request.data["contentType"] for types in ['application/base64', 'image/png', 'image/jpeg']]):
					post.image_content = request.data["content"]
				else:
					post.content = request.data["content"]

				# Serialize the data retrieved from the table
				serializer = self.get_serializer(post)

				# Return the updated post
				return Response(serializer.data, status=status.HTTP_200_OK)
			except:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			# If the author or post could not be found from the request data and the authentication provided, return a 403 Forbidden
			return Response(status=status.HTTP_403_FORBIDDEN, data="User cannot modify this post!")
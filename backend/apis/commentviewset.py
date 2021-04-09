import requests
from manager.paginate import ResultsPagination
from manager.settings import HOSTNAME
from ..models import Author, Comment, Inbox, Node, Post
from ..serializers import CommentSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from ..utils import add_post, get_author_by_ID

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

	pagination_class = ResultsPagination

	def create(self, request, author_id=None, post_id=None, *args, **kwargs):
		"""
		This method creates a comment for a post, taking in the author ID for the author of the post ID.
		"""

		# Parse the ID
		print(request.data, request.body)
		comment_author_id = request.data['author']['url'].split('/')[-1]
		print(request.data, request.body)
		# Check if the author already exists in the database
		try:
			print(comment_author_id)
			comment_author, comment_author_isLocal = get_author_by_ID(request, comment_author_id, "author")
		# If no user exists create an author
		except:
			return Response(data="Could not find the comments author on the server!", status=status.HTTP_404_NOT_FOUND)

		# Can't do this because the posts author is not included in the request
		# try:
		# 	post_author, post_author_isLocal = get_author_by_ID(request, author_id, "author")
		# except:
		# 	return Response("Could not find the post's author on the server!", status=status.HTTP_404_NOT_FOUND)
		remote_comments_link = request.data.get("comments", None)

		if not comment_author_isLocal:
			try:
				post = Post.objects.filter(id=post_id).get()
				if not HOSTNAME in post.origin:
					raise Exception

			# Return a 404 as the post does not exist
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)

		elif comment_author_isLocal: # Here we check if the post exists in our databse already, if it doesn't then we need to send a request for the post. Once we get the post we can create the comment on our server and the remote server
			# Check if the post exists in the database
			try:
				post = Post.objects.filter(id=post_id).get() #TODO: Double check if the post is remote spent
				if not HOSTNAME in post.origin:
					raise Exception
			# Post is not a local post so send the request through to the other server
			except Exception as e:
				try:
					if remote_comments_link:
						comment_host = remote_comments_link.split('/')[2]
						node = Node.objects.filter(host__icontains=comment_host).get()
						s = requests.Session()
						s.auth = (node.remote_username, node.remote_password)
						s.headers.update({'Content-Type':'application/json'})
						response_comment = s.post(node.host+"author/"+author_id+"/posts/"+post_id, json=request.body)
					else:
						raise Exception("The comment link of the remote post is not present!")
				except:
					return Response(data="Unable to send the comment to the remote server!", status=status.HTTP_400_BAD_REQUEST)
				else:
					if response_comment.status_code in [200, 201]:
						return Response(response_comment.json(), status=response_comment.status_code)
					else:
						return Response(data="The remote server encountered an error creating the comment!", status=response_comment.status_code)






		# Create a new comment object, this will only run if the comment author is local and the post author is local or if the comment author is remote but the post author is local
		comment = Comment(
			author = comment_author,
			post = post,
			comment = request.data["comment"],
			contentType = request.data["contentType"],
			host = HOSTNAME,
			post_author_id = author_id
		)
		comment.save()


		# Issue an inbox object to the post author
		inbox = Inbox(
			author = post.author,
			icomment = comment
		)
		inbox.save()

		serializer = self.get_serializer(comment)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def list(self, request, author_id=None, post_id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the comment endpoint. This will retrieve the posts comment list and return the response.
		"""

		if request.user.is_authenticated:
			if post_id:
				# Set the pagination class for the returned comments
				self.pagination_class = ResultsPagination

				# Filter the comment table using the post id that is passed in the requests url
				comments = Comment.objects.filter(post=post_id).order_by('-published')

				# See if the query returned any results, if not return a 404
				if not comments:
					return Response(status=status.HTTP_404_NOT_FOUND, data="Could not find the Comments for the Post provided")

				# Get the serializer and serialize the returned comment table rows
				serializer = self.get_serializer(comments, many=True)

				# Paginate the serialized queryset
				paginated_serializer_data = self.paginate_queryset(serializer.data)

				# Return the paginated and serialized data
				return Response(paginated_serializer_data, status=status.HTTP_200_OK)
			else:
				# Return 400 Bad Request if the post id could not be retrieved form the requests url
				return Response(status=status.HTTP_400_BAD_REQUEST, data="Unable to parse the post id from the request")
		else:
			# Return 403 forbidden if the request is not authenticated
			return Response(status=status.HTTP_403_FORBIDDEN)
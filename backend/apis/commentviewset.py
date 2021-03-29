from manager.paginate import ResultsPagination
from manager.settings import HOSTNAME
from ..models import Author, Comment, Inbox, Post
from ..serializers import CommentSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

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

		# Check if the post exists in the database
		try:
			post = Post.objects.filter(id=post_id).get()
		# Return a 404 as the post does not exist
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# Parse the ID
		comment_author_id = request.data['author']['id'].split('/')[-1]
		# Check if the author already exists in the database
		try:
			comment_author = Author.objects.filter(id=comment_author_id).get()
		# If no user exists create an author
		except:
			comment_author = Author(
							id = comment_author_id,
							user = request.user,
							displayName = request.data['author']['displayName'],
							github = request.data['author']['github'],
							host = request.data['author']['host'],
							url = request.data['author']['url'],
							)
			comment_author.save()

		# Create a new comment object
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
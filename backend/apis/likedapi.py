from ..models import Author, Like
from ..serializers import LikeSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

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


	def list(self, request, author_id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint. This will retrieved the user's post list and return the response.
		"""
		# If the requesting user is pro
		if request.user.is_authenticated:
			# If an author name is passed
			if author_id:
				# Query likes table for all likes by the author
				likes = Like.objects.filter(author=author_id, post__visibility="PUBLIC")
				serializer = self.get_serializer(likes, many=True)

				return Response({"type":"liked", "items": serializer.data}, status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)


	def get_serializer_context(self):
		"""
		This method adds the display name of the author to the context for serializing.
		"""
		context = super().get_serializer_context()
		context['displayName'] = Author.objects.filter(user=self.request.user.id).get().displayName
		return context
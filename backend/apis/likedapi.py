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
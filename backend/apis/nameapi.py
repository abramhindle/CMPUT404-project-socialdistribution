from ..models import Author
from ..serializers import AuthorSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response


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
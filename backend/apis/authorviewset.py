from ..models import Author
from ..serializers import AuthorSerializer

from rest_framework.response import Response
from rest_framework import permissions, status, viewsets

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

	def update(self, request, id=None,*args, **kwargs):
		"""
		This method will be called when a POST request is received for a specific author to update the information for the author.
		"""

		author = Author.objects.filter(user=request.user.id).get()
		checkDisplay = Author.objects.filter(displayName=request.data["displayName"]).get()

		# If the display name already exists
		if checkDisplay and checkDisplay.id != author.id:
			return Response(data="Display name already exists", status=status.HTTP_409_CONFLICT)

		# If no ID is passed in the request
		if id == None:
			return Response(data="ID required", status=status.HTTP_400_BAD_REQUEST)

		# If the request is authenticated and the ID pass matches the requesting user
		if request.user.is_authenticated and author.id == id:
			# Update the display name and github
			author.displayName = request.data["displayName"]
			author.github = request.data["github"]
			author.save()
			# Respond with the updated author object and a 200 status
			return Response(self.get_serializer(author).data, status=status.HTTP_200_OK)
		# If the request is not valid or the ID does not match the requesting user
		else:
			return Response(data="Not authorized to modify this author",status=status.HTTP_403_FORBIDDEN)
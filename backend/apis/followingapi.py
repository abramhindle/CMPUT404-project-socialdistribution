from ..models import Author, Follow
from ..serializers import AuthorSerializer, FollowSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

class FollowingAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the a list of authors you are following. This will run methods to retrieve DB rows and return correctly formatted HTTP responses
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
	queryset = Follow.objects.filter(friends=True)

	def list(self, request, author_id=None, *args, **kwargs):
		'''
		This method retreives a list of Authors who are following a specified Author by their author_id.
		'''

		# Check if the id passed is a valid author, else send a 404
		try:
			check = Author.objects.filter(id=author_id).get()
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# If the request is authenticated
		if request.user.is_authenticated:

			output = []
			# Get a list of follow objects for the id
			follows = Follow.objects.filter(follower=author_id)

			# Check all follow objects
			for follow in follows.iterator():
				# Get the Author object for the follower
				author = Author.objects.filter(id=follow.followee.id).get()
				# Serialize the data
				serialized = AuthorSerializer(author)
				output.append(serialized.data)

			# Return the list of followers
			return Response({
				"type": "friends",
				"items": output
			})
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

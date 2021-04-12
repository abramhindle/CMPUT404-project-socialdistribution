from ..models import Author, Follow, Like, Post
from ..serializers import LikeSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

class LikeAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the Like objects. This will run methods to retrieve and edit DB rows and return correctly formatted HTTP responses
	"""

	# Specifies the permissions required to access the data
	permission_classes = [
		permissions.IsAuthenticated
	]

	# Specifies the field used for querying the DB
	lookup_field = 'id'

	# Specifies the serializer used to return a properly formatted JSON response body
	serializer_class = LikeSerializer

	# Specifies the query set of Post objects that can be returned
	queryset = Like.objects.all()

	def list(self, request, author_id=None, post_id=None, comment_id=None, *args, **kwargs):
		"""
		This method is run in the case that a GET request is retrieved by the API for the post endpoint. This will retrieved the user's like list and return the response.
		"""

		# If the required author ID and post ID are not passed
		if author_id is None or post_id is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		# Check if the post is friends only
		try:
			if Post.objects.filter(id=post_id).get().visibility == 'FRIENDS':
				# Check if the requesting user is friends with the post author
				try:
					check_friends = Follow.objects.filter(follower__user=request.user, followee=author_id, friends=True)
					if not check_friends:
						return Response(data="It appears you are not a friend and are trying to view a friends-only posts information!", status=status.HTTP_403_FORBIDDEN)
				except Exception as e:
					return Response(str(e), status=status.HTTP_403_FORBIDDEN)
		except:
			return Response(data="Could not find the post specified in the url!", status=status.HTTP_404_NOT_FOUND)
		# Check if the request is for a comment
		try:
			if comment_id:
				likes = Like.objects.filter(post=post_id, comment=comment_id)
				serializer = self.get_serializer(likes, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				likes = Like.objects.filter(post=post_id)
				serializer = self.get_serializer(likes, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			return Response(data="Ran into an issue retrieving the likes for that object! " +str(e), status=status.HTTP_404_NOT_FOUND)

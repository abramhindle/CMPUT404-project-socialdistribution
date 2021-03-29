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
		# If the user is authenticated
		if request.user.is_authenticated:
			# If the required author ID and post ID are not passed
			if author_id and post_id:
				# Get the author object for the request user
				user_author = Author.objects.filter(user=request.user.id).get()
				# Check if the post is friends only
				if Post.objects.filter(id=post_id).get().visibility == 'FRIENDS':
					# Check if the requesting user is friends with the post author
					try:
						check_friends = Follow.objects.filter(follower=user_author.id, followee=author_id, friends=True).get()
					except:
						return Response(status=status.HTTP_403_FORBIDDEN)
				# Check if the request is for a comment
				if comment_id:
					likes = Like.objects.filter(post=post_id, comment=comment_id)
					serializer = self.get_serializer(likes, many=True)
					return Response(serializer.data, status=status.HTTP_200_OK)
				else:
					likes = Like.objects.filter(post=post_id)
					serializer = self.get_serializer(likes, many=True)
					return Response(serializer.data, status=status.HTTP_200_OK)
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
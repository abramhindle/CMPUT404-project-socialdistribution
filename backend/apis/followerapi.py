from ..models import Author, Follow, Inbox, Node
from ..serializers import AuthorSerializer, FollowSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
import json

class FollowerAPI(viewsets.ModelViewSet):
	"""
	This class specifies the view for the a list of Followers for an Author. This will run methods to retrieve DB rows and return correctly formatted HTTP responses
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
	queryset = Follow.objects.all()

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
			follows = Follow.objects.filter(followee=author_id)

			# Check all follow objects
			for follow in follows.iterator():
				# Get the Author object for the follower
				author = Author.objects.filter(id=follow.follower.id).get()
				# Serialize the data
				serialized = AuthorSerializer(author)
				output.append(serialized.data)

			# Return the list of followers
			return Response({
				"type": "followers",
				"items": output
			})
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def destroy(self, request, author_id=None, foreign_id=None, *args, **kwargs):
		"""
		This method is used to delete a follow, either the follower or followee can delete a follow.
		"""
		# Try to get the follower and followee from our Authors table, if they do not exist, return a 404 to state that the follow does not exist
		try:
			followee = Author.objects.filter(id=author_id).get()
			follower = Author.objects.filter(id=foreign_id).get()
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# Check that the user is authenticated, also make sure that the requester is the authenticated user associated with the author object
		if request.user.is_authenticated and (request.user == followee.user or request.user == follower.user): 
			if author_id and foreign_id: # Ensure that the URL does contain the correct ids

				# Try to retrieve the follow record from the DB, return 404 if it does not exist
				try:
					follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
				except:
					return Response(status=status.HTTP_404_NOT_FOUND)

				# If the authors were friends, unfriend the followee
				if follow.friends == True:
					followee.friends = False
					followee.save()

				# Get the follow to be deleted to return it to the requester
				deleted_follow = self.get_serializer(follow)

				# If the follow record exists, delete it
				if follow:
					follow.delete()

				# Return the serializer output data as the response
				return Response(deleted_follow.data, status=status.HTTP_200_OK)
			else:
				# Return 400 if the request is missing the followers id or the followees id
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			# Return 403 if the requester doe snot have the correct authentication to delete the follow record
			return Response(status=status.HTTP_403_FORBIDDEN)

	def create(self, request, author_id=None, foreign_id=None, *args, **kwargs):
		'''
		This method creates a new follow between two authors.
		'''

		# Decode the request body and load into a json
		body = json.loads(request.body.decode('utf-8'))

		# Check if the foreign ID exists in the database, if not add that Author to our database
		try:
			foreign_author = Author.objects.filter(id=foreign_id).get()
		except:
			foreign_author = Author(
				id = foreign_id,
				user = request.user,
				displayName = body["actor"]["displayName"],
				github = body["actor"]["github"],
				host = body["actor"]["host"],
				url = body["actor"]["url"]
			)
			foreign_author.save()

		# Check if the user is authenticated, and if the user is the one following or is from a valid node
		if request.user.is_authenticated and (Node.objects.filter(local_username=request.user.username) or Author.objects.filter(user=request.user.id).get().id == foreign_id):

			# Check that an author id and foreign id are passed in
			if body["object"]["id"].endswith(author_id) and body["actor"]["id"].endswith(foreign_id):

				# Check if a follow between the two authors already exists
				try:
					follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
					return Response(status=status.HTTP_409_CONFLICT)
				except:
					pass
				# Get both author objects, or return a 404
				try:
					actor = Author.objects.filter(id=foreign_id).get()
					object = Author.objects.filter(id=author_id).get()
				except:
					return Response(status=status.HTTP_404_NOT_FOUND)
				# Check if the follower is already being followed by the followee
				check_follow = Follow.objects.filter(follower=object, followee=actor)

				# If a follow does exist then set their relationship as being friends and create a follow
				if check_follow:
					follow = Follow(
						follower=actor,
						followee=object,
						friends = True,
						summary=actor.displayName + " wants to follow " + object.displayName
					)
					check_follow.update(friends=True)
				# Else just create a follow
				else:
					follow = Follow(
						follower=actor,
						followee=object,
						summary=actor.displayName + " wants to follow " + object.displayName
					)
				follow.save()
				serializer = self.get_serializer(follow)
				# Create an object to be added to the inbox of the author being followed
				inbox = Inbox(
					author=object,
					follow=follow
				)
				inbox.save()

				# Return the follow object that was created
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			# If the body information is mismatched from the url
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		# The user was not authenticated
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def retrieve(self, request, author_id=None, foreign_id=None, *args, **kwargs):
		"""
		Method to check if a follow exists, and return that follow object. Returns a 404 if the follow does not exist.
		"""

		# Try to retrieve the follower and followee from the authors table
		try:
			followee = Author.objects.filter(id=author_id).get()
			follower = Author.objects.filter(id=foreign_id).get()
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# Check that the requester is authenticated, also make sure that the requester is the associated authenticated user to one of the authors
		if request.user.is_authenticated and (request.user == followee.user or request.user == follower.user):

			# Check that the author_id and foreign_id are present in the url
			if author_id and foreign_id:

				# Try to get the follow record of the two authors to return
				try:
					follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
					return Response(self.get_serializer(follow).data, status=status.HTTP_200_OK)
				except:
					# Return a 404 if the record was not found
					return Response(status=status.HTTP_404_NOT_FOUND)
			else:
				# Return a 400 if the author_id or foreign_id could not be found in the url
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			# Return a 403 if proper authentication and permissions could not be verified
			return Response(status=status.HTTP_403_FORBIDDEN)
from ..models import Author, Follow, Inbox, Node
from ..serializers import AuthorSerializer, FollowSerializer
from .. import utils

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
		# Check that the ID in the body matches the request URL
		if not body["object"]["id"].endswith(author_id) or not body["actor"]["id"].endswith(foreign_id):
			return Response(data="Body does not match URL!",status=status.HTTP_400_BAD_REQUEST)

		# Check that the requesting user is authenticated
		if request.user.is_authenticated:
			# Check if the follow already exists
			try:
				follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
				return Response(data="Already following this author!", status=status.HTTP_409_CONFLICT)
			except:
				pass

			# Get the author objects for actor/object
			try:
				actor_author, isLocal_actor = utils.get_author_by_ID(request, foreign_id, "actor")
				object_author, isLocal_object = utils.get_author_by_ID(request, author_id, "object")
			except Exception as e:
				return Response(data=str(e), status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(data="Not authorized", status=status.HTTP_403_FORBIDDEN)

		# Check if the follower is already being followed by the followee
		check_follow = Follow.objects.filter(follower=object_author, followee=actor_author)
		# Create the follow
		follow = Follow(
					follower=actor_author,
					followee=object_author,
					summary=actor_author.displayName + " wants to follow " + object_author.displayName
					)
		follow.save()
		# If a follow does exist then set their relationship as being friends and create a follow
		if check_follow:
			follow.update(friends=True)
			check_follow.update(friends=True)

		# Serialize the follow object
		serialized_follow = self.get_serializer(follow)


		if isLocal_actor and actor_author.user == request.user:
			# If the object is local to the server
			if isLocal_object:
				# Create an object to be added to the inbox of the author being followed
				inbox = Inbox(
						author=object_author,
						follow=follow
						)
				inbox.save()
			else:
				# Send the follow to the remote server and send to their inbox
				node = Node.objects.filter(user=object_author.user).get()
				s = requests.Session()
				s.auth = (node.remote_username, node.remote_password)
				s.headers.update({'Content-Type':'application/json'})
				#print("POST to:", node.host+"author/"+follower.follower.id+"/inbox", json=serializer.data)
				response = s.post(node.host+"author/"+follower.follower.id+"/inbox", json=serializer.data)
				except:
					# Create the post in the inbox of the friend if the friend is local to the server
					inbox = Inbox(
						author = follower.follower,
						post = post
					)
					inbox.save()




		# # Check if a follow between the two authors already exists
		# try:
		# 	follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
		# 	return Response(status=status.HTTP_409_CONFLICT)
		# except:
		# 	pass
		
		
		# Get both author objects, or return a 404
		# try:
		# 	actor = Author.objects.filter(id=foreign_id).get()
		# 	object = Author.objects.filter(id=author_id).get()
		# except:
		# 	return Response(status=status.HTTP_404_NOT_FOUND)
	
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
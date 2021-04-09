from ..models import Author, Follow, Inbox, Node
from ..serializers import AuthorSerializer, FollowSerializer
from .. import utils

import requests
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

				try:
					reverse_follow = Follow.objects.filter(followee=foreign_id, follower=author_id).get()
				except:
					reverse_follow = False

				# If the authors were friends, unfriend the followee
				if follow.friends == True and reverse_follow:
					reverse_follow.friends = False
					reverse_follow.save()

				# Get the follow to be deleted to return it to the requester
				deleted_follow = self.get_serializer(follow)
				is_remote_followee = False
				try:
					node = Node.objects.filter(user=followee.user).get()
					is_remote_followee = True
					s = requests.Session()
					s.auth = (node.remote_username, node.remote_password)
					s.headers.update({'Content-Type':'application/json'})
					response_follow = s.delete(node.host+"author/"+followee.id+"/followers/"+follower.id)
				except:
					is_remote_followee = False


				# If the follow record exists, delete it
				if not is_remote_followee or (is_remote_followee and response_follow.status_code in [200]):
					if follow:
						follow.delete()
				else:
					reverse_follow.friends = True
					reverse_follow.save()
					return Response(data="Was not able to delete the follow in the followee's server!", status=status.HTTP_404_NOT_FOUND)

				# Return the serializer output data as the response
				return Response(deleted_follow.data, status=status.HTTP_200_OK)
			else:
				# Return 400 if the request is missing the followers id or the followees id
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			# Return 403 if the requester does not have the correct authentication to delete the follow record
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

				if not isLocal_actor and not isLocal_object:
					actor_author.delete()
					object_author.delete()
					raise Exception("Neither author is on our server!")
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
		# If a follow does exist then set their relationship as being friends and create a follow
		if check_follow:
			follow.friends = True
			check_follow.update(friends=True)
		follow.save()

		# Serialize the follow object
		serialized_follow = self.get_serializer(follow)

		# Check if the actor is local and the requesting user
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
				# Send the follow to the remote server
				node = Node.objects.filter(user=object_author.user).get()
				s = requests.Session()
				s.auth = (node.remote_username, node.remote_password)
				s.headers.update({'Content-Type':'application/json'})
				url = node.host+"author/"+object_author.id+"/followers/"+actor_author.id
				if 'konnection' in node.host:
					url += '/'
				response_follow = s.put(url, json=serialized_follow.data)

				if not response_follow.status_code in [200, 201]:
					follow.delete()
					if check_follow:
						check_follow.update(friends=False)

					return Response(data="Follow not accepted by remote host", status=status.HTTP_400_BAD_REQUEST)
		# If the actor is not local and is the requesting user
		elif not isLocal_actor and actor_author.user == request.user:
			# If the object is local to the server
			if isLocal_object:
				# Create an object to be added to the inbox of the author being followed
				inbox = Inbox(
						author=object_author,
						follow=follow
						)
				inbox.save()
			else:
				return Response(data="Neither author is on our server!", status=status.HTTP_404_NOT_FOUND)
		else:
			return Response(data="Requesting user is not authorized to make this follow", status=status.HTTP_403_FORBIDDEN)

		# Return the follow object that was created
		return Response(serialized_follow.data, status=status.HTTP_201_CREATED)

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
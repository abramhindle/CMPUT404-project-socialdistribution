
from ..models import Author, Node
from ..serializers import AuthorSerializer
from manager.settings import HOSTNAME

import requests
import json
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

	def list(self, request, *args, **kwargs):
		"""
		This method will be called when a GET request is received, listing all the authors in the database.
		"""
		# Check if query parameters are passed in the URL
		if request.query_params.get('more') and request.user.node.remote_username == "":
			nodes = Node.objects.all()
			local_authors = Author.objects.filter(host=HOSTNAME)
			data = []
			data += self.get_serializer(local_authors, many=True).data
			for node in nodes.iterator():
				s = requests.Session()
				s.auth = (node.remote_username, node.remote_password)
				print("GET to:", node.host+"authors")
				response = s.get(node.host+"authors")
				data += response.json()
		else:
			authors = Author.objects.filter(host=HOSTNAME)
			data = self.get_serializer(authors, many=True).data
		# Respond with a serialized list of authors
		return Response(data, status=status.HTTP_200_OK)


	def update(self, request, id=None,*args, **kwargs):
		"""
		This method will be called when a POST request is received for a specific author to update the information for the author.
		"""

		try:
			# Decode the request body and load into a json
			body = json.loads(request.body.decode('utf-8'))
		except:
			return Response("Unable to parse the JSON body", status=status.HTTP_400_BAD_REQUEST)

		# Check if the author exists for the requesting user
		if Author.objects.filter(user=request.user.id):
			try:
				author = Author.objects.filter(user=request.user.id, id=id).get()
			except:
				return Response(data="Not authorized to modify this author",status=status.HTTP_403_FORBIDDEN)
		# The user is not authorized to modify this author
		else:
			return Response(data="Author does not exist", status=status.HTTP_404_NOT_FOUND)

		# Check if the displayName already exists on the server
		try:
			checkDisplay = Author.objects.filter(displayName=body["displayName"]).get()
			if checkDisplay.id != author.id:
				return Response(data="Display name already exists!", status=status.HTTP_409_CONFLICT)
		except:
			pass

		# Update the display name and github
		author.displayName = body["displayName"]
		author.github = body["github"]
		author.save()
		# Respond with the updated author object and a 200 status
		return Response(self.get_serializer(author).data, status=status.HTTP_200_OK)

from django.db.models.query import RawQuerySet
from ..models import Author, Follow, Inbox, Node
from ..serializers import AuthorSerializer, FollowSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
import base64

import socket, sys, logging, json

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

		if request.user.is_authenticated:

			output = []
			follows = Follow.objects.filter(followee=author_id)

			for follow in follows.iterator():

				author = Author.objects.filter(id=follow.follower.id).get()

				serialized = AuthorSerializer(author)
				output.append(serialized.data)

			return Response({
				"type": "followers",
				"items": output
			})
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)

	def destroy(self, request, author_id=None, foreign_id=None, *args, **kwargs):

		if author_id and foreign_id:
			try:
				follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
			except:
				return Response(status.HTTP_404_NOT_FOUND)

			deleted_follow = self.get_serializer(follow)

			if follow:
				follow.delete()

			# Return the serializer output data as the response
			return Response(deleted_follow.data, status=status.HTTP_200_OK)

		return super().destroy(request, *args, **kwargs)

	def create(self, request, author_id=None, foreign_id=None, *args, **kwargs):


		body = json.loads(request.body.decode('utf-8'))

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

		if request.user.is_authenticated and (Author.objects.filter(user=request.user.id).get().id == author_id or Node.objects.filter(local_username=request.user.username)):

			if author_id and foreign_id:
				try:
					follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
					return Response(status.HTTP_409_CONFLICT)
				except:
					pass

				try:
					actor = Author.objects.filter(id=foreign_id).get()
					object = Author.objects.filter(id=author_id).get()

				except:
					return Response(status.HTTP_404_NOT_FOUND)

				check_follow = Follow.objects.filter(follower=object, followee=actor)


				if check_follow:
					follow = Follow(
						follower=actor,
						followee=object,
						friends = True,
						summary=actor.displayName + " wants to follow " + object.displayName
					)
					check_follow.update(friends=True)

				else:
					follow = Follow(
						follower=actor,
						followee=object,
						summary=actor.displayName + " wants to follow " + object.displayName
					)
				follow.save()
				serializer = self.get_serializer(follow)

				inbox = Inbox(
					author=object,
					follow=follow
				)
				inbox.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)

		else:
			return Response(status.HTTP_403_FORBIDDEN)

	def retrieve(self, request, author_id=None, foreign_id=None, *args, **kwargs):

		if request.user.is_authenticated and Author.objects.filter(user=request.user.id).get().id == author_id:

			if author_id and foreign_id:
				try:
					follow = Follow.objects.filter(followee=author_id, follower=foreign_id).get()
					return Response(self.get_serializer(follow).data, status=status.HTTP_200_OK)
				except:
					return Response(status.HTTP_404_NOT_FOUND)
			else:
				return Response(status.HTTP_400_BAD_REQUEST)
		else:
			return Response(status.HTTP_403_FORBIDDEN)
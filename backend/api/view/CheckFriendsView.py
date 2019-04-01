import urllib

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .Util import get_local_friends_list
from ..models import Follow, AuthorProfile
from .Util import get_author_id
import json


class CheckFriendsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, authorid):
        if (self.kwargs['authorid'] == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        author_profile = AuthorProfile.objects.filter(id=authorid)
        if (len(author_profile) != 1):
            return Response("Error: Author Does Not Exist", status.HTTP_400_BAD_REQUEST)

        full_author_id = get_author_id(author_profile[0], False)

        response_data = {
            "query": "friends",
            "authors": get_local_friends_list(full_author_id)
        }
        return Response(response_data, status.HTTP_200_OK)

    def post(self, request, authorid):
        try:
            if (self.kwargs['authorid'] == ""):
                return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

            author_profile = AuthorProfile.objects.filter(id=authorid)
            if (len(author_profile) != 1):
                return Response("Error: Author Does Not Exist", status.HTTP_400_BAD_REQUEST)

            full_author_id = get_author_id(author_profile[0], False)
            friends_list = []
            for friend in get_local_friends_list(full_author_id):
                for friend_in_data in request.data.getlist("authors"):
                    if friend_in_data == friend:
                        friends_list.append(friend_in_data)
                        break

            response_data = {
                "query": "friends",
                "author": full_author_id,
                "authors": friends_list
            }
            return Response(response_data, status.HTTP_200_OK)
        except Exception as e:
            return Response("Error", status.HTTP_400_BAD_REQUEST)
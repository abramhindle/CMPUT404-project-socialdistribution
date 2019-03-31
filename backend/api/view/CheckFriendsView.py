import urllib

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .Util import get_local_friends_list
from ..models import Follow, AuthorProfile
from .Util import get_author_id


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

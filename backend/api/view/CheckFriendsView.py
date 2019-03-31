import urllib

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow, AuthorProfile
from ..serializers import AuthorProfileSerializer


class CheckFriendsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, authorid):
        if (self.kwargs['authorid'] == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        author_profile = AuthorProfile.objects.filter(id=authorid)
        if (len(author_profile) != 1):
            return Response("Error: Author Does Not Exist", status.HTTP_400_BAD_REQUEST)

        full_author_id = AuthorProfileSerializer(author_profile[0]).data["id"]

        friends_list = Follow.objects.filter(authorA=full_author_id, status="FRIENDS")
        response_authors = []

        for friend in friends_list:
            response_authors.append(friend.authorB)

        response_data = {
            "query": "friends",
            "authors": response_authors
        }
        return Response(response_data, status.HTTP_200_OK)

import urllib

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow, AuthorProfile
from ..serializers import FriendsListSerializer, AuthorProfileSerializer


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
        friends_serialized_data = FriendsListSerializer(friends_list, many=True).data
        response_authors = []

        for ele in friends_serialized_data:
            response_authors.append(friends_serialized_data[0]["authorB"])

        response_data = {
            "query": "friends",
            "authors": response_authors
        }
        return Response(response_data, status.HTTP_200_OK)

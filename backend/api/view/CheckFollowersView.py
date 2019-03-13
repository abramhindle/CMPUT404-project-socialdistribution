import urllib

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow, AuthorProfile
from ..serializers import FollowersListSerializer


class CheckFollowersView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, authorid):
        if (self.kwargs['authorid'] == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)
        author_id = urllib.parse.unquote(self.kwargs['authorid'])
        tmp = author_id.split("author/")
        print(tmp)
        if (len(tmp) == 2):
            query_set = AuthorProfile.objects.filter(host=tmp[0], id=tmp[1])
            if (len(query_set) != 1):
                return Response("Error: Author Does Not Exist", status.HTTP_400_BAD_REQUEST)
        friends_list = Follow.objects.filter(authorB=author_id, status="FOLLOWING")
        friends_serialized_data = FollowersListSerializer(friends_list, many=True).data
        response_authors = []

        for ele in friends_serialized_data:
            response_authors.append(friends_serialized_data[0]["authorA"])

        response_data = {
            "query": "followers",
            "authors": response_authors
        }
        return Response(response_data, status.HTTP_200_OK)

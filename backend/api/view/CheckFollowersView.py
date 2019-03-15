import urllib

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow, AuthorProfile
from ..serializers import AuthorProfileSerializer


class CheckFollowersView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, authorid):
        if (self.kwargs['authorid'] == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        author_profile = AuthorProfile.objects.filter(id=authorid)
        if (len(author_profile) != 1):
            return Response("Error: Author Does Not Exist", status.HTTP_400_BAD_REQUEST)

        full_author_id = AuthorProfileSerializer(author_profile[0]).data["id"]

        follow_list = Follow.objects.filter(authorB=full_author_id, status="FOLLOWING")

        follow_list_data = []
        for follower in follow_list:
            follower_fulll_id = follower.authorA
            tmp_follower_data = follower_fulll_id.split("author/")
            host = tmp_follower_data[0]
            follower_author_profile_id = tmp_follower_data[1]
            # todo: check if host belongs to our server, call cross server endpoint if doesnt
            follower_profile = AuthorProfile.objects.get(id=follower_author_profile_id)
            serialized_author_profile = AuthorProfileSerializer(follower_profile)

            follow_list_data.append(serialized_author_profile.data)

        response_data = {
            "query": "followers",
            "authors": follow_list_data
        }
        return Response(response_data, status.HTTP_200_OK)

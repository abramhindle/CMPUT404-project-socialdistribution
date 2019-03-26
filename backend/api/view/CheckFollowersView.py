from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow, AuthorProfile, ServerUser
from ..serializers import AuthorProfileSerializer
import requests
import json
from urllib.parse import urlparse
from django.conf import settings


class CheckFollowersView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, authorid):
        if (self.kwargs['authorid'] == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        parsed_url = urlparse(authorid)
        author_host = '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)

        follow_list_data = []

        for follower in Follow.objects.filter(authorB=authorid, status="FOLLOWING"):
            follower_fulll_id = follower.authorA
            tmp_follower_data = follower_fulll_id.split("author/")
            follower_host = tmp_follower_data[0]
            follower_author_profile_id = tmp_follower_data[1]

            if author_host == follower_host:
                follower_profile = AuthorProfile.objects.get(id=follower_author_profile_id)
                serialized_author_profile = AuthorProfileSerializer(follower_profile)
                follow_list_data.append(serialized_author_profile.data)
            else:
                try:
                    server_user = ServerUser.objects.get(host=follower_host)

                    # todo update the username, password, prefix to by from model
                    url = "{}api/author/{}".format(server_user.host, follower_author_profile_id)
                    my_cross_server_username = settings.USERNAME
                    my_cross_server_password = settings.PASSWORD
                    headers = {'Content-type': 'application/json'}
                    response = requests.get(url,
                                            auth=(my_cross_server_username, my_cross_server_password),
                                            headers=headers)
                    if response.status_code == 200:
                        follow_list_data.append(json.loads(response.content))
                    else:
                        print("not 200")
                        print(response.content)
                except Exception as e:
                    # ignore and just not add into follower list if cant get from server
                    print("died")
                    print(e)
                    pass

        response_data = {
            "query": "followers",
            "authors": follow_list_data
        }
        return Response(response_data, status.HTTP_200_OK)

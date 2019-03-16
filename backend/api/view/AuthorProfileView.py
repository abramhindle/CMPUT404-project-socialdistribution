from django.db import transaction
from rest_framework import generics
from rest_framework import authentication, permissions, status
from ..serializers import AuthorProfileSerializer
from rest_framework.response import Response
from ..models import AuthorProfile, Follow


class AuthorProfileView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    mutable_keys = ["displayName", "github", "bio", "firstName", "lastName", "email"]

    def is_mutable(self, key):
        for ele in self.mutable_keys:
            if(key == ele):
                return True
        return False

    def post(self, request, uid):
        authorId = self.kwargs['uid']

        if(authorId == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)
        
        else:
            try:
                author_to_update = AuthorProfile.objects.filter(id=uid)
                if(not author_to_update.exists()):
                    return Response("Error: Author does not exist", status.HTTP_400_BAD_REQUEST)
                author_to_update = author_to_update[0]
                if(request.user.authorprofile.id != author_to_update.id):
                    return Response("Error: You do not have permission to edit this profile", status.HTTP_400_BAD_REQUEST)
                else:
                    for key, value in request.data.items():
                        if self.is_mutable(str(key)):
                            if(value == None):
                                error_message = "Error: {} cannot have value as None".format(key)
                                return Response(error_message, status.HTTP_400_BAD_REQUEST)
                            setattr(author_to_update, key, value)
                        else:
                            error_message = "Error: Can't modify {}".format(key)
                            return Response(error_message, status.HTTP_400_BAD_REQUEST)

                    author_to_update.full_clean()
                    author_to_update.save()
                    return Response("Success: Successfully updated profile", status.HTTP_200_OK)
            except:
                return Response("Error: Update Profile Fail", status.HTTP_400_BAD_REQUEST)

    def get(self, request, uid):
        authorId = self.kwargs['uid']
        if(authorId == ""):
            return Response("Error: Author ID required!", status.HTTP_400_BAD_REQUEST)

        query_set = AuthorProfile.objects.filter(id=authorId)

        if (len(query_set) == 1):
            response_data = AuthorProfileSerializer(query_set[0]).data

            friends = Follow.objects.filter(authorA=response_data["id"], status="FRIENDS")
            friends_list_data = []
            for ele in friends:
                friend_fulll_id = ele.authorB
                tmp = friend_fulll_id.split("author/")
                host = tmp[0]
                short_id = tmp[1]
                # todo: check if host belongs to our server, call cross server endpoint if doesnt
                friend_profile = AuthorProfile.objects.get(id=short_id)
                serialized_author_profile = AuthorProfileSerializer(friend_profile)

                friends_list_data.append(serialized_author_profile.data)

            response_data["friends"] = friends_list_data

            return Response(response_data, status.HTTP_200_OK)
        
        else:
            return Response("Author does not exist", status.HTTP_400_BAD_REQUEST)

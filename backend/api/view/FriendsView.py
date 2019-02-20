from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow


def valid_input(data):
    try:
        assert (data["query"] == "friendrequest")
        if (len(data["author"]["id"]) == 0 or len(data["friend"]["id"]) == 0):
            return False
    except:
        return False
    return True


class FriendsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if (valid_input(request.data)):
            existing_follow = Follow.objects.filter(authorA=request.data["friend"]["id"],
                                                    authorB=request.data["author"]["id"],
                                                    status="FOLLOWING")
            if (existing_follow.exists()):
                Follow.objects.create(authorA=request.data["author"]["id"],
                                      authorB=request.data["friend"]["id"],
                                      status="FRIENDS")

                existing_follow.update(status="FRIENDS")
            else:
                # create if does not exist
                Follow.objects.get_or_create(authorA=request.data["author"]["id"],
                                             authorB=request.data["friend"]["id"],
                                             status="FOLLOWING")
            return Response("Friend Request Success", status.HTTP_200_OK)
        else:
            return Response("Invalid Input", status.HTTP_400_BAD_REQUEST)

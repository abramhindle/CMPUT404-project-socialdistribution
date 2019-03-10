from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow


def valid_input(data):
    try:
        if (len(data["query"]) == 0 or
                len(data["author"]["id"]) == 0 or
                len(data["friend"]["id"]) == 0):
            return False
    except:
        return False
    return True


# function to follow or be friend
def follow(data):
    existing_follow = Follow.objects.filter(authorA=data["friend"]["id"],
                                            authorB=data["author"]["id"],
                                            status="FOLLOWING")
    if (existing_follow.exists()):
        Follow.objects.create(authorA=data["author"]["id"],
                              authorB=data["friend"]["id"],
                              status="FRIENDS")

        existing_follow.update(status="FRIENDS")
    else:
        # create if does not exist
        Follow.objects.get_or_create(authorA=data["author"]["id"],
                                     authorB=data["friend"]["id"],
                                     status="FOLLOWING")
    return Response("Friend Request Success", status.HTTP_200_OK)


# function to unfriend
def unfriend(data):
    response_message = "Unfriend Request Success"
    status_code = status.HTTP_200_OK
    existing_friend = Follow.objects.filter(authorA=data["friend"]["id"],
                                            authorB=data["author"]["id"],
                                            status="FRIENDS")
    if (existing_friend.exists()):
        existing_friend.delete()
    else:
        response_message = "Unfriend Request Fail"
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(response_message, status_code)


class FriendsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if (valid_input(request.data)):
            if (request.data["query"] == "friendrequest"):
                return follow(request.data)
            elif (request.data["query"] == "unfriend"):
                return unfriend(request.data)
            else:
                return Response('Invalid query type, must be "friendrequest" or "unfriend"',
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid Input", status.HTTP_400_BAD_REQUEST)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow, AuthorProfile


def valid_input(data):
    try:
        if (len(data["query"]) == 0 or
                len(data["author"]["id"]) == 0 or
                len(data["friend"]["id"]) == 0):
            return False
    except:
        return False
    return True


def valid_author(request):
    try:
        tmp = request.data["author"]["id"].split("author/")
        author_host = tmp[0]
        # todo check if host is local when cross server
        author_short_id = tmp[1]

        tmp = request.data["friend"]["id"].split("author/")
        friend_host = tmp[0]
        # todo check if host is local when cross server
        friend_short_id = tmp[1]

        request_user = AuthorProfile.objects.filter(user=request.user)
        if not (request_user.exists() and
                AuthorProfile.objects.filter(id=friend_short_id).exists() and
                str(request_user[0].id) == str(author_short_id)):
            return False
    except:
        return False
    return True


# function to follow or be friend
def follow(request):
    if(valid_author(request)):
        data = request.data
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
        return Response("Follow Request Success", status.HTTP_200_OK)
    else:
        return Response("Follow Request Fail", status.HTTP_400_BAD_REQUEST)


# function to unfollow
def unfollow(request):
    if (valid_author(request)):
        data = request.data
        existing_follow = Follow.objects.filter(authorA=data["author"]["id"],
                                                authorB=data["friend"]["id"])
        if (existing_follow.exists()):
            if(existing_follow[0].status == "FRIENDS"):
                existing_friend = Follow.objects.get(authorA=data["friend"]["id"],
                                                        authorB=data["author"]["id"],
                                                        status="FRIENDS")
                setattr(existing_friend, "status", "FOLLOWING")
                existing_friend.save()
            existing_follow.delete()

            return Response("Unfollow Request Success", status.HTTP_200_OK)
        else:
            return Response("Unfollow Request Fail", status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Unfollow Request Fail", status.HTTP_400_BAD_REQUEST)


class FriendsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if (valid_input(request.data)):
            if (request.data["query"] == "friendrequest"):
                return follow(request)
            elif (request.data["query"] == "unfollow"):
                return unfollow(request)
            else:
                return Response('Invalid query type, must be "friendrequest" or "unfollow"',
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Invalid Input", status.HTTP_400_BAD_REQUEST)

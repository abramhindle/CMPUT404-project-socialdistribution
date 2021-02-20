from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import Author, Follow
from socialdistribution.serializers import AuthorSerializer

@api_view(['GET'])
def follower_list(request, authorID): # GET: get a list of authors who are their followers
    pk = Author.objects.get(authorID=authorID)
    friend_object, created = Follow.objects.get_or_create(current_user=pk)
    #  if friend != request.user.userprofile
    followers = []
    for f in friend_object.users.all():
        serializer = AuthorSerializer(f)
        followers.append(serializer.data)
    return Response({"type": "followers","items":followers}, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT'])
def follower(request, authorID, foreignAuthorID):
    if request.method == "GET": # check if follower
        if foreignAuthorID in Follow.objects.followers(authorID):
            return Response({'message':"True"}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"False"}, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        pass

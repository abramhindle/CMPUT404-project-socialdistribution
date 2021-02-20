from friendship.models import Friend, Follow, FriendshipRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import Author
from socialdistribution.serializers import RegistrationSerializer, AuthorSerializer

@api_view(['GET'])
def friend_list(request, authorID):
    return {'friends': Friend.objects.requests(authorID)}

@api_view(['GET'])
def follower_list(request, authorID):
    return {'followers': Follow.objects.followers(authorID)}

@api_view(['GET', 'DELETE', 'PUT'])
def follower(request, authorID, foreignAuthorID):
    if request.method == "GET": # check if follower
        if foreignAuthorID in Follow.objects.followers(authorID):
            return Response({'message':"True"}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"False"}, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        

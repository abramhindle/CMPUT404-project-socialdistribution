from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import *
from socialdistribution.serializers import *

@api_view(['GET'])
def friend(request, authorID):
    author = Author.objects.get(authorID=authorID)
    friend_object, created = Follow.objects.get_or_create(current_user=author)
    friends = []
    for f in friend_object.users.all(): # foreach follower f or author
        friend_object_1, created = Follow.objects.get_or_create(current_user=f) # get the followers of f
        if author in friend_object_1.users.all(): # check if author is also a follower of f
            serializer = AuthorSerializer(f)
            friends.append(serializer.data)
    return Response({"type": "friends","items":friends}, status=status.HTTP_200_OK)

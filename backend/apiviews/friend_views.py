from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import views, status
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from backend.serializers import UserSerializer, FriendSerializer, FriendRequestSerializer
from backend.models import User, Friend, FriendRequest
from backend.permissions import *
from rest_framework.decorators import action
from django.http import Http404
from django.db.models import Q
import json


class FriendViewSet(views.APIView):
    """Make a friend request to a user"""
    serializer_class = FriendSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        '''
        /friend/accept: Set freindship between fromUser and toUser
        '''

        # print(dict(request.data))
        request_data = dict(request.data)
        if (request_data.get("query") == "friend"):
            user_id = request_data["fromUser"].get("id").rsplit('/', 1)[1]
            friend_id = request_data["toUser"].get("id").rsplit('/', 1)[1]
            user = get_object_or_404(User, pk=int(user_id))
            friend = get_object_or_404(User, pk=int(friend_id))
            if not Friend.objects.filter(fromUser=user, toUser=friend).exists() or not Friend.objects.filter(fromUser=friend, toUser=user):
                serializer = FriendSerializer(data=request_data, context={
                    "fromUser": user,  "toUser": friend})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"query": "createFriend", "success": True, "message": "Friendship created"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"query": "createFriend", "success": False, "message": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({"query": "createFriend", "success": False, "message": "Already Friends"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({"query": "createFriend", "success": False, "message": "wrong request"}, status=status.HTTP_400_BAD_REQUEST)

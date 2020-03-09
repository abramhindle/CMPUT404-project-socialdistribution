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
from backend.utils import *


class FriendViewSet(views.APIView):
    """Friendships between two users"""
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def make_friend(self, user, friend):
        '''
        our model needs two relationships in the table: Author + Friend (and vice versa)
        '''
        Friend.objects.create(
            fromUser=user, toUser=friend).save()
        Friend.objects.create(
            fromUser=friend, toUser=user).save()
        # delete the friend request
        FriendRequest.objects.filter(
            fromUser__fullId=user.fullId).delete()

    def post(self, request):
        '''
        /friend/accept: Set freindship between author and friend
        '''
        request_data = dict(request.data)
        if (request_data.get("query") == "friend"):
            # grab the userids and friend
            user_id = request.user.fullId
            friend_id = protocol_removed(request_data["toUser"].get("id"))
            # check if friend request was made
            if FriendRequest.objects.filter(toUser__fullId=user_id, fromUser__fullId=friend_id).exists():
                # get user and friend object
                user = get_object_or_404(User, fullId=user_id)
                friend = get_object_or_404(User, fullId=friend_id)
                # check if they are already friends
                if not Friend.objects.filter(fromUser=user, toUser=friend).exists() or not Friend.objects.filter(fromUser=friend, toUser=user):
                    # make them friends
                    self.make_friend(user, friend)
                    return Response({"query": "createFriend", "success": True, "message": "Friendship created"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"query": "createFriend", "success": False, "message": "Already Friends"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({"query": "createFriend", "success": False, "message": "No Friend Request"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({"query": "createFriend", "success": False, "message": "wrong request"}, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from rest_framework import viewsets,status,exceptions
from .serializers import FriendSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from .models import Friend
from .permissions import OwnerOrAdminPermissions
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# Create your views here.
class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    permission_classes = [OwnerOrAdminPermissions]
    lookup_field = "id"

    def get_queryset(self):
        return self.request.user.f1Ids.filter(status='A')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FriendSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        authenticated_user = str(request.user)
        f1Id = request.data.get('f1Id',None)
        f2Id = request.data['f2Id']
        user_status = request.data.get('status',None)

        if f1Id != None and f1Id != authenticated_user:
            msg = _("You cannot update friend request for others")
            raise exceptions.ValidationError(msg)

        if authenticated_user == f2Id:
            msg = _("You cannot update friend request with yourself")
            raise exceptions.ValidationError(msg)

        if user_status == "A":
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

        if not Friend.objects.filter(f1Id_id=authenticated_user,f2Id_id=f2Id).exists():
            msg = _("You need to make friend request first")
            raise exceptions.ValidationError(msg)

        elif user_status == "R":
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            msg = ("The status has to be either A or R")
            raise exceptions.ValidationError(msg)

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    permission_classes = [OwnerOrAdminPermissions]
    lookup_field = "id"

    def get_queryset(self):
        return self.request.user.f1Ids.filter(status='U')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        authenticated_user = str(request.user)
        f1Id = request.data.get('f1Id',None)
        f2Id = request.data['f2Id']
        user_status = request.data.get('status',None)

        if f1Id != None and f1Id != authenticated_user:
            msg = _("You cannot make friend request for others")
            raise exceptions.ValidationError(msg)

        if authenticated_user == f2Id:
            msg = _("You cannot make friend request with yourself")
            raise exceptions.ValidationError(msg)

        if Friend.objects.filter(f1Id_id=f2Id,f2Id_id=authenticated_user).exists():
            msg = _("You cannot make friend request because you are friends already")
            raise exceptions.ValidationError(msg)

        if user_status != None and user_status != 'U':
            msg = ("You cannot make friend request with this status")
            raise exceptions.ValidationError(msg)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(f1Id=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FriendSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        authenticated_user = str(request.user)
        f1Id = request.data.get('f1Id',None)
        f2Id = request.data['f2Id']
        user_status = request.data.get('status',None)

        if f1Id != None and f1Id != authenticated_user:
            msg = _("You cannot update friend request for others")
            raise exceptions.ValidationError(msg)

        if authenticated_user == f2Id:
            msg = _("You cannot update friend request with yourself")
            raise exceptions.ValidationError(msg)

        if user_status == "A":
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

        if not Friend.objects.filter(f1Id_id=authenticated_user,f2Id_id=f2Id).exists():
            msg = _("You need to make friend request first")
            raise exceptions.ValidationError(msg)

        elif user_status == "R":
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            msg = ("The status has to be either A or R")
            raise exceptions.ValidationError(msg)
    


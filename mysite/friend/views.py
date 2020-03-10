from django.shortcuts import render
from rest_framework import viewsets, status, exceptions
from .serializers import FriendSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from .models import Friend
from .permissions import AdminOrF1Permissions, AdminOrF2Permissions
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# Create your views here.
class IfFriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    lookup_url_kwarg = "f2Id"

    def retrieve(self, request, *args, **kwargs):
        authenticated_user = str(request.user)
        username = self.kwargs.get(self.lookup_url_kwarg)

        if Friend.objects.filter(f1Id_id=authenticated_user, f2Id_id=username).exists():
            friend = Friend.objects.get(f1Id_id=authenticated_user, f2Id_id=username)
            if friend.status == "U":
                response = Response({"status": "pending"}, status=status.HTTP_200_OK)
            elif friend.status == "A":
                response = Response({"status": "friend"}, status=status.HTTP_200_OK)
            elif friend.status == 'R':
                response = Response({"status": "unfriend"}, status=status.HTTP_200_OK)

        elif Friend.objects.filter(
            f1Id_id=username, f2Id_id=authenticated_user
        ).exists():
            friend = Friend.objects.get(f1Id_id=username, f2Id_id=authenticated_user)
            if friend.status == "U":
                response = Response({"status": "pending"}, status=status.HTTP_200_OK)
            elif friend.status == "A":
                response = Response({"status": "friend"}, status=status.HTTP_200_OK)
            elif friend.status == 'R':
                response = Response({"status": "unfriend"}, status=status.HTTP_200_OK)
        else:
            response = Response({"status": "unfriend"}, status=status.HTTP_200_OK)

        return response

class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    lookup_field = "id"

    def get_queryset(self):
        return self.request.user.f1Ids.filter(
            status="A"
        ) | self.request.user.f2Ids.filter(status="A")

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update", "partial_update"]:
            self.permission_classes = [AdminOrF1Permissions | AdminOrF2Permissions]
        else:
            self.permission_classes = [IsAdminUser]

        return super(FriendViewSet, self).get_permissions()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["f2Id"] = str(request.user)
        serializer = FriendSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        authenticated_user = str(request.user)
        f1Id = request.data.get("f1Id", None)
        f2Id = request.data.get("f2Id", None)
        friend_status = request.data.get("status", None)

        if f1Id == f2Id:
            msg = _("You cannot remove friend with yourself")
            raise exceptions.ValidationError(msg)

        if friend_status == "R":
            if (
                Friend.objects.filter(f1Id_id=f1Id, f2Id_id=authenticated_user).exists()
                or Friend.objects.filter(
                    f1Id_id=authenticated_user, f2Id_id=f1Id
                ).exists()
            ):
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                msg = _("You need to make friend request first")
                raise exceptions.ValidationError(msg)
        else:
            msg = "You cannot update friend friend request with this status"
            raise exceptions.ValidationError(msg)


class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    lookup_field = "id"

    def get_queryset(self):
        return self.request.user.f2Ids.filter(status="U")

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update", "partial_update"]:
            self.permission_classes = [AdminOrF2Permissions]
        elif self.action in ["create"]:
            self.permission_classes = [AdminOrF1Permissions]
        else:
            self.permission_classes = [IsAdminUser]

        return super(FriendRequestViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        request.data["f1Id"] = str(request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        authenticated_user = str(request.user)
        f1Id = request.data.get("f1Id", None)
        f2Id = request.data.get("f2Id", None)
        friend_status = request.data.get("status", None)

        if f1Id != authenticated_user:
            msg = _("You cannot make friend request for others")
            raise exceptions.ValidationError(msg)

        if authenticated_user == f2Id:
            msg = _("You cannot make friend request with yourself")
            raise exceptions.ValidationError(msg)

        if Friend.objects.filter(f1Id_id=f2Id, f2Id_id=authenticated_user).exists():
            msg = _("You cannot make friend request because you are friends already")
            raise exceptions.ValidationError(msg)

        if friend_status != None and friend_status != "U":
            msg = "You cannot make friend request with this status"
            raise exceptions.ValidationError(msg)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(f1Id=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["f2Id"] = str(request.user)
        serializer = FriendSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        authenticated_user = str(request.user)
        f1Id = request.data.get("f1Id", None)
        f2Id = request.data.get("f2Id", None)
        user_status = request.data.get("status", None)

        if f2Id != None and f2Id != authenticated_user:
            msg = _("You cannot update friend request for others")
            raise exceptions.ValidationError(msg)

        if authenticated_user == f1Id:
            msg = _("You cannot update friend request with yourself")
            raise exceptions.ValidationError(msg)

        if not Friend.objects.filter(f1Id_id=f1Id, f2Id_id=authenticated_user).exists():
            msg = _("You need to make friend request first")
            raise exceptions.ValidationError(msg)

        if user_status == "A":
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif user_status == "R":
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            msg = "The status has to be either A or R"
            raise exceptions.ValidationError(msg)

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FriendSerializer
from .models import Friend
from .permissions import OwnerPermissions
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# Create your views here.
class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    permission_classes = [IsAdminUser | OwnerPermissions]
    lookup_field = "id"
    queryset = Friend.objects.filter(status='A')


class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    permission_classes = [IsAdminUser | OwnerPermissions]
    lookup_field = "id"
    queryset = Friend.objects.filter(status='U')

    def perform_create(self, serializer):
        serializer.save(f1Id=self.request.user)


    


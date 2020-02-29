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

    def get_queryset(self):
        return self.request.user.f1Ids.all()

    def perform_create(self, serializer):
        serializer.save(f1Id=self.request.user)


    


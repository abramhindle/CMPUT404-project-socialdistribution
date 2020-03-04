from django.shortcuts import render
from rest_framework import viewsets,status
from .serializers import FriendSerializer
from rest_framework.response import Response
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
        return self.request.user.f1Ids.filter(status='A')

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    permission_classes = [IsAdminUser | OwnerPermissions]
    lookup_field = "id"

    def get_queryset(self):
        return self.request.user.f1Ids.filter(status='U')

    def perform_create(self, serializer):
        serializer.save(f1Id=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data['status'] == "A":
            serializer = FriendSerializer(instance=instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.data['status'] == "R":
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        


    


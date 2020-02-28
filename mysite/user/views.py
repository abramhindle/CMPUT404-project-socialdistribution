from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .serializers import AuthorSerializer
from .models import User
from .permissions import OwnerOrAdminPermissions

# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    # add authentication to this view
    # user can only use this view with valid token
    queryset = User.objects.filter(is_superuser=0)
    lookup_field = "username"

    # used to update the author's profile
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AuthorSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update", "create"]:
            self.permission_classes = [OwnerOrAdminPermissions]
        else:
            self.permission_classes = [AllowAny]
        return super(AuthorViewSet, self).get_permissions()

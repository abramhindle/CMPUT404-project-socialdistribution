from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action

from user.models import User
from .models import Comment
from .serializer import CommentSerializer


class OwnerOrAdminPermission(permissions.BasePermission):
    message = "You must be the owner of the comment."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_staff


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_field = "id"

    def get_queryset(self):
        return self.request.user.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            self.permission_classes = [
                OwnerOrAdminPermission,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super(CommentViewSet, self).get_permissions()

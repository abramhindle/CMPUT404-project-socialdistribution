from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from authors.models import Author
from .serializers import NotificationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from backend.permissions import IsOwnerOrAdmin


class IsPostOwnerOrAdmin(IsOwnerOrAdmin):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj: Notification):
        return obj.author.profile


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "notifications", 'items': data})


class NotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomPageNumberPagination
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        author = self.kwargs["author"]
        return Notification.objects.filter(author__local_id=author).order_by("-published")

    def retrieve(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, id=self.kwargs["pk"])
        return Response(NotificationSerializer(notification).data)

    def destroy(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, id=self.kwargs["pk"])
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        serializer.save(author=author)

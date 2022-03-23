from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from authors.models import Author
from .serializers import NotificationSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from backend.permissions import IsOwnerOrAdmin


class IsNotificationOwnerOrAdmin(IsOwnerOrAdmin):
    """Only Allow Owners Or Admins To Access The Object"""

    @staticmethod
    def get_owner(obj: Notification):
        return obj.author.profile


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "notifications", 'items': data})


class NotificationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsNotificationOwnerOrAdmin]
    pagination_class = CustomPageNumberPagination
    serializer_class = NotificationSerializer

    def get_queryset(self):
        author = self.kwargs["author"]
        queryset = Notification.objects.filter(author__local_id=author).order_by("-published")
        for q in queryset:
            self.check_object_permissions(self.request, q)
        return queryset

    def perform_create(self, serializer):
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        serializer.save(author=author)

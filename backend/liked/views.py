from urllib import response
from django.http import Http404
from rest_framework.pagination  import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import LikesSerializer
from posts.models import Post
from authors.models import Author
from .models import Likes
from rest_framework import status
from rest_framework.decorators import action


class LikedPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        if not data:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'type': "Liked", 'items': data})

# Create your views here.
class LikedRetrievedViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = LikedPagination
    serializer_class = LikesSerializer
    def get_queryset(self):
        targetUrl = get_object_or_404(Author, local_id=self.kwargs["author"])
        return Likes.objects.filter(author_url=targetUrl.local_id).order_by('author_url')
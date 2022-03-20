
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

# from backend.likes import serializers


class LikesPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({'type': "Like", 'items': data})


class LikesViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = LikesPagination
    serializer_class = LikesSerializer


    def get_queryset(self):
        targetUrl = str(self.request.build_absolute_uri())[:-6].replace("/api", "")
        try:
            if Likes.objects.filter(object=targetUrl):
                return Likes.objects.filter(object=targetUrl)
        except:
            return Http404


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        # summary = author.displayName + "like your post"
        serializer.save(author_url=author.id)
    

    # def perform_destroy(self, instance):
        
    #     print ("I am cccb")

    
    # def destroy(self, request, *args, **kwargs):
    #     print("*****")
    #     targetUrl = str(self.request.build_absolute_uri())[:-6].replace("/api", "")
    #     print("*****")
    #     print(targetUrl)
    #     try:
    #         like = Likes.objects.get(object=targetUrl)
    #         like.delete()
    #     except:
    #         return Http404
        

    # def destroy(self, request, *args, **kwargs):
    #     post = self.kwargs["post"]
    #     print("post id########### is: ", post)
    #     try:
    #         instance = Likes.objects.get(object=post)
    #         instance.delete()
    #     except:
    #         pass
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['update', 'create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

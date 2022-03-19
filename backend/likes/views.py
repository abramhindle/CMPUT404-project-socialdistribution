
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
        post = self.kwargs["post"]
        print("#post is: ", post)
        return Likes.objects.filter(object = post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, local_id=self.kwargs["post"])
        author = get_object_or_404(Author, local_id=self.kwargs["author"])
        serializer.save(author_url=author.id, post=post)
    
    # def perform_destroy(self, instance):
    #     if instance.type == 'userdefined':
    #         instance.delete()
    # def perform_destroy(self): 
    #         # write custom code
    #     print("##########################")
    # def destroy(self, request, *args, **kwargs):
    #     print("dsfdsfadfadsfadsafadfadsf")
    #     post = self.kwargs["post"]
    #     print("post id########### is: ", post)
    #     instance = Likes.objects.get(object=post)
    #     self.perform_destroy(instance)

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

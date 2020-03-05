from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from backend.serializers import PostSerializer
from backend.models import Post
from backend.permissions import *


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for all the operation related to Post
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "postId"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(visibility=PUBLIC)

        # TODO add pagination
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        '''
        /posts/{POST_ID} : access to a single post with id = {POST_ID}
        '''
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"query": "posts", "count": 1, "size": 1, "post": [serializer.data]})

    def create_post(self, request, *args, **kwargs):
        '''
        /author/posts : create a post for currently authenticated user
        '''
        post_data = dict(request.data)

        if post_data:
            '''
            Our model takes in a pk rather than Json, since only this endpoint will only be used by logged in user,
            therefore, we just grab the id from request after they authenticated successfully
            '''
            post_data["author"] = self.request.user.id
            serializer = PostSerializer(
                data=post_data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"query": "createPost", "success": True, "message": "Post created"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"query": "createPost", "success": False, "message": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"query": "createPost", "success": False, "message": "wrong request"},
                            status=status.HTTP_400_BAD_REQUEST)

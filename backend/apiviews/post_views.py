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
from backend.apiviews.paginations import PostPagination


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for all the operation related to Post
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "postId"
    pagination_class = PostPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(visibility=PUBLIC)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        '''
        GET /posts/{POST_ID} : access to a single post with id = {POST_ID}
        '''
        instance = self.get_object()
        queryset = Post.objects.none()
        queryset |= Post.objects.filter(pk=instance.pk).order_by("pk")

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        '''
        DELETE /posts/{POST_ID} : delete post with id = {POST_ID}
        '''
        post_id = self.kwargs.get(self.lookup_field)
        deleted_post = get_object_or_404(Post, pk=post_id)

        if deleted_post.author.id == request.user.id:
            self.perform_destroy(deleted_post)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"success": False, "msg": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def create_post(self, request, *args, **kwargs):
        '''
        POST /author/posts : create a post for currently authenticated user
        '''

        post_data = request.data
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

    def get_user_visible_posts(self, request):
        user = request.user
        visible_posts = Post.objects.none()

        for post in self.get_queryset():
            if user in post.get_visible_users():
                visible_posts |= Post.objects.filter(postId=post.postId)

        page = self.paginate_queryset(visible_posts.order_by('-timestamp'))
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)

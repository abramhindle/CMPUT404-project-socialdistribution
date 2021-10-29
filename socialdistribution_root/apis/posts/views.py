# Using serializers and Rest framework:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404

from socialdistribution.permissions import IsOwnerOrReadOnly 
from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from apps.core.models import User

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

# TODO permissions for public/private

# Used for formatting and styling responses
def compose_posts_dict(query_type, data):
    json_result = {
        'query': query_type,
        'data': data
    }

    return json_result


class post(GenericAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    
    def get_object(self):
        # Validate given author
        get_object_or_404(User.objects.all(), pk=self.kwargs["author_id"])

        # Validate and retrieve post
        post = get_object_or_404(self.get_queryset(), pk=self.kwargs["post_id"])

        # Check User permission to edit post
        self.check_object_permissions(self.request, post)
        return post

    def get_author(self):
        # Validate given author
        author = get_object_or_404(User.objects.all(), pk=self.kwargs["author_id"])
        return author

    # GET get the public post
    def get(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        post = self.get_object()
        serializer = PostSerializer(post)
        formatted_data = compose_posts_dict(query_type="GET on post", data=serializer.data)

        return Response(formatted_data)

    # POST update the post (must be authenticated)
    def post(self, request: HttpRequest, author_id: str, post_id: str):
        post = self.get_object()
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # set uri post id for json response
            post = self.get_object()
            post.set_post_id(request.get_host())
            post.save()

            # serialize saved post for response
            serializer = PostSerializer(post)
            formatted_data = compose_posts_dict(query_type="POST on post", data=serializer.data)

            return Response(formatted_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT create a post with that post_id
    def put(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        # validate given author_id
        user = self.get_author()

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.create(
                    id=post_id,
                    author=user, 
                    **serializer.validated_data
                )
            # set uri post id for json response
            post.set_post_id(request.get_host())
            post.save()

            # serialize saved post for response
            serializer = PostSerializer(post)
            formatted_data = compose_posts_dict(query_type="PUT on post", data=serializer.data)

            return Response(formatted_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE remove the post
    def delete(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        post = self.get_object()
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class posts(GenericAPIView):
    permission_classes = [IsOwnerOrReadOnly]

    # This is being used to paginate queryset
    serializer_class = PostSerializer

    def get_author(self):
        # Validate given author
        author = get_object_or_404(User.objects.all(), pk=self.kwargs["author_id"])
        return author

    # GET get recent posts of author (paginated)
    def get(self, request: HttpRequest, author_id: str):
        author = self.get_author()

        # filter out only posts by given author and paginate
        queryset = Post.objects.filter(author_id=author.id)
        queryset = self.filter_queryset(queryset)
        one_page_of_data = self.paginate_queryset(queryset)

        serializer = self.get_serializer(one_page_of_data, many=True)
        dict_data = compose_posts_dict(query_type="GET on posts", data=serializer.data)
        result = self.get_paginated_response(dict_data)

        return JsonResponse(result.data, safe=False)

    # POST create a new post but generate a post_id
    def post(self, request: HttpRequest, author_id: str):
        # validate given author_id
        user = self.get_author()

        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = Post.objects.create(
                author=user, 
                **serializer.validated_data
            )
            # set uri post id for json response
            post.set_post_id(request.get_host())
            post.save()

            # serialize saved post for response
            serializer = PostSerializer(post)
            formatted_data = compose_posts_dict(query_type="POST on posts", data=serializer.data)

            return Response(formatted_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class comments(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str, post_id: str):
         

# Examples of calling api
# author uuid(replace): "582b3b39-e455-4e7b-88e2-3df2d7d35995"
# post uuid(replace): "f3589e1a-5533-5b7b-abd6-81b6187af7ce"
# Authentication admin(replace): "YWRtaW46YWRtaW4=" (admin:admin)
# Bad Authentication admin(replace): "YWRtaW4yOmFkbWluMg==" (admin2:admin2)
    # GET post
    #     curl http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f3589e1a-5533-5b7b-abd6-81b6187af7ce/ 
    
    # Put post
    #     curl -X PUT http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f3589e1a-5533-5b7b-abd6-81b6187af7ce/  -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
    # "type":"post",
    # "title":"A post posted with put api on /post/",
    # "description":"This post discusses stuff -- brief",
    # "contentType":"text/plain",
    # "author":{
    #       "type":"author",
    #       "id":"582b3b39-e455-4e7b-88e2-3df2d7d35995"
    # },
    # "visibility":"PUBLIC",
    # "unlisted":false}'  

    # POST post
    #     curl -X POST http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f3589e1a-5533-5b7b-abd6-81b6187af7ce/  -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
    # "type":"post",
    # "title":"A post that was changed by POST with api /post/"}'  

    # Delete post
    # curl -X DELETE http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/f3589e1a-5533-5b7b-abd6-81b6187af7ce/ -H "Authorization: Basic YWRtaW46YWRtaW4="
    # 
    #--------------------------------------------------------------------
    # 
    # GET posts
    # curl http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/ 
    
    #  GET posts with pagination
    # curl "http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/?page=2&size=3"  

    # POST posts
    #  comment ->                                                                                                                                           | That is base64 | encoded "admin:admin" below
    #     curl -X POST http://localhost:8000/author/582b3b39-e455-4e7b-88e2-3df2d7d35995/posts/ -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
    # "type":"post",
    # "title":"A post title about a post about web dev",
    # "description":"This post discusses stuff -- brief",
    # "contentType":"text/markdown",
    # "author":{
    #       "type":"author",
    #       "id":"582b3b39-e455-4e7b-88e2-3df2d7d35995"
    # },
    # "visibility":"PUBLIC",
    # "unlisted":false}'     
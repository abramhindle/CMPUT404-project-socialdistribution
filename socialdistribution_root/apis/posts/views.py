# Using serializers and Rest framework:
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

from django.http import JsonResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from socialdistribution.permissions import IsOwnerOrReadOnly 
from apps.posts.models import Comment, Post
from apps.posts.serializers import CommentSerializer, PostSerializer
from apps.core.models import Author

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from socialdistribution.utils import Utils

# TODO permissions for public/private

class post(GenericAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    
    def get_object(self):
        # Validate given author
        try:
            get_object_or_404(Author.objects.all(), pk=self.kwargs["author_id"])
        except: 
            raise Http404()

        # Validate and retrieve post
        try:
            post = get_object_or_404(self.get_queryset(), pk=self.kwargs["post_id"])
        except: 
            raise Http404()

        # Check Author permission to edit post
        self.check_object_permissions(self.request, post)
        return post

    def get_author(self):
        # Validate given author
        try:
            author = get_object_or_404(Author.objects.all(), pk=self.kwargs["author_id"])
        except: 
            raise Http404()

        return author

    # GET get the public post
    def get(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        post = self.get_object()
        serializer = PostSerializer(post)
        formatted_data = Utils.formatResponse(query_type="GET on post", data=serializer.data)

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
            formatted_data = Utils.formatResponse(query_type="POST on post", data=serializer.data)

            return Response(formatted_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT create a post with that post_id
    def put(self, request: HttpRequest, author_id: str, post_id: str, format=None):
        # validate given author_id
        author = self.get_author()

        try:
            # if the post exists already, we'll throw 400
            self.get_object()
            return HttpResponseBadRequest("a post with that id already exists")
        except Http404: # there shouldn't be a post with this id yet
            pass

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = Post.objects.create(
                    id=post_id,
                    author=author, 
                    **serializer.validated_data
                )
            # set uri post id for json response
            post.set_post_id(request.get_host())
            post.save()

            # serialize saved post for response
            serializer = PostSerializer(post)
            formatted_data = Utils.formatResponse(query_type="PUT on post", data=serializer.data)

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
        try:
            author = get_object_or_404(Author.objects.all(), pk=self.kwargs["author_id"])
            return author
        except:
            raise Http404()

    # GET get recent posts of author (paginated)
    def get(self, request: HttpRequest, author_id: str):
        author = self.get_author()

        # filter out only posts by given author and paginate
        queryset = Post.objects.filter(author=author_id)
        queryset = self.filter_queryset(queryset)
        one_page_of_data = self.paginate_queryset(queryset)

        serializer = self.get_serializer(one_page_of_data, many=True)
        dict_data = Utils.formatResponse(query_type="GET on posts", data=serializer.data)
        result = self.get_paginated_response(dict_data)

        return JsonResponse(result.data, safe=False)

    # POST create a new post but generate a post_id
    def post(self, request: HttpRequest, author_id: str):
        # validate given author_id
        author = self.get_author()

        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = Post.objects.create(
                author=author, 
                **serializer.validated_data
            )
            # set uri post id for json response
            post.set_post_id(request.get_host())
            post.save()

            # serialize saved post for response
            serializer = PostSerializer(post)
            formatted_data = Utils.formatResponse(query_type="POST on posts", data=serializer.data)

            return Response(formatted_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class comments(GenericAPIView):
    def get(self, request: HttpRequest, author_id: str, post_id: str):
        host = request.scheme + "://" + request.get_host()
        comments = Comment.objects.filter(author=author_id, post=post_id)
        one_page_of_data = self.paginate_queryset(comments)
        serializer = CommentSerializer(one_page_of_data, context={'host': host}, many=True)
        dict_data = Utils.formatResponse(query_type="GET on comments", data=serializer.data)
        result = self.get_paginated_response(dict_data)
        return JsonResponse(result.data, safe=False)

    def post(self, request: HttpRequest, author_id: str, post_id: str):
        author: Author = None
        try:
            author: Author = Author.objects.get(pk=author_id)
        except:
            return HttpResponseNotFound()
        
        post: Post = None
        try:
            post: Author = Post.objects.get(pk=post_id)
        except:
            return HttpResponseNotFound()

        if (author and post):
            host = request.scheme + "://" + request.get_host()

            data = JSONParser().parse(request)
            serializer = CommentSerializer(data=data)

            if (serializer.is_valid()):
                comment = Comment.objects.create(
                    author=author,
                    post=post,
                    **serializer.validated_data)

                comment.save()

                serializer = CommentSerializer(comment, context={'host': host})
                formatted_data = Utils.formatResponse(query_type="POST on comments", data=serializer.data)
                return Response(formatted_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseNotFound()


# Examples of calling api
# author uuid(replace): "4f890507-ad2d-48e2-bb40-163e71114c27"
# post uuid(replace): "d57bbd0e-185c-4964-9e2e-d5bb3c02841a"
# Authentication admin(replace): "YWRtaW46YWRtaW4=" (admin:admin)
# Bad Authentication admin(replace): "YWRtaW4yOmFkbWluMg==" (admin2:admin2)

    # GET post
    #     curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/ 
    
    # PUT post
    #     curl -X PUT http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/  -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
    # "type":"post",
    # "title":"A post posted with put api on /post/",
    # "description":"This post discusses stuff -- brief",
    # "contentType":"text/plain",
    # "author":{
    #       "type":"author",
    #       "id":"4f890507-ad2d-48e2-bb40-163e71114c27"
    # },
    # "visibility":"PUBLIC",
    # "unlisted":false}'  

    # POST post
    #     curl -X POST http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/  -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
    # "type":"post",
    # "title":"A post that was changed by POST with api /post/"}'  

    # DELETE post
    # curl -X DELETE http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/ -H "Authorization: Basic YWRtaW46YWRtaW4="
    # 
    #--------------------------------------------------------------------
    # 
    # GET posts
    # curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/ 
    
    #GET posts with pagination
    # curl "http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/?page=2&size=3"  

    # POST posts
    #  comment ->                                                                                                                                           | That is base64 | encoded "admin:admin" below
    #     curl -X POST http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/ -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
    # "type":"post",
    # "title":"A post title about a post about web dev",
    # "description":"This post discusses stuff -- brief",
    # "contentType":"text/markdown",
    # "author":{
    #       "type":"author",
    #       "id":"4f890507-ad2d-48e2-bb40-163e71114c27"
    # },
    # "visibility":"PUBLIC",
    # "unlisted":false}' 

    # GET comments
    # curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/comments 

    # POST comments
    # curl http://localhost:8000/author/4f890507-ad2d-48e2-bb40-163e71114c27/posts/d57bbd0e-185c-4964-9e2e-d5bb3c02841a/comments -H "Content-Type: application/json" -H "Authorization: Basic YWRtaW46YWRtaW4=" -d '{
    # "type":"comment",
    # "author":{
    #     "type":"author",
    #     "id":"4f890507-ad2d-48e2-bb40-163e71114c27"
    # },
    # "comment":"A Comment with words and markdown",
    # "contentType":"text/markdown"
    # }'
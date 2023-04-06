from django.http import HttpResponseRedirect
from author.basic_auth import BasicAuthenticator
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from django.views import generic
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .serializers import *
from .pagination import PostSetPagination
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import (
                                        HTMLFormRenderer, 
                                        JSONRenderer, 
                                        BrowsableAPIRenderer,
                                    )
import base64
import json
from client import *
from .image_renderer import JPEGRenderer, PNGRenderer


custom_parameter = openapi.Parameter(
    name='custom_param',
    in_=openapi.IN_QUERY,
    description='A custom parameter for the POST request',
    type=openapi.TYPE_STRING,
    required=True,
)

response_schema_dictposts = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": {
    "results": [
        {
            "type": "post",
            "title": "Funny post",
            "id": "5ad63a2b-4890-47b8-bc24-979a96941863",
            "description": "This is a funny joke. Laugh.",
            "contentType": "text/plain",
            "content": "I tried to catch fog the other day, I Mist.",
            "author": {
                "type": "author",
                "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
                "displayName": "Fahad",
                "url": "",
                "profileImage": ""
            },
            "categories": [
                "Funny"
            ],
            "comments": "/comments/",
            "published": "2023-03-03T14:45:41.208691-07:00",
            "visibility": "PUBLIC"
        },
        {
            "type": "post",
            "title": "Sad post",
            "id": "3e227dbd-986f-4f3b-9872-2f81d9c6335f",
            "description": "Sad post,Cry",
            "contentType": "text/plain",
            "content": "Hi this is very sad :(",
            "author": {
                "type": "author",
                "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
                "displayName": "Fahad",
                "url": "",
                "profileImage": ""
            },
            "categories": [
                "Sad"
            ],
            "comments": "/comments/",
            "published": "2023-03-03T14:47:10.782792-07:00",
            "visibility": "PUBLIC"
        }
    ]
}
        }
        
    )}

response_schema_dictpost = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": {
    "type": "post",
    "title": "Sad post",
    "id": "3e227dbd-986f-4f3b-9872-2f81d9c6335f",
    "description": "Sad post,Cry",
    "contentType": "text/plain",
    "content": "Hi this is very sad :(",
    "author": {
        "type": "author",
        "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
        "displayName": "Fahad",
        "url": "",
        "profileImage": ""
    },
    "categories": [
        "Sad"
    ],
    "comments": "/comments/",
    "published": "2023-03-03T14:47:10.782792-07:00",
    "visibility": "PUBLIC"
}
        }
        
    )}

response_schema_dictdelete = {
    
    "204":openapi.Response(description="Successful Deletion",)}


response_schema_dictComments = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": [
    {
        "type": "comment",
        "author": {
            "type": "author",
            "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
            "displayName": "Fahad",
            "url": "",
            "profileImage": ""
        },
        "comment": "Wow haha funny dude!",
        "contentType": "text/plain",
        "published": "2023-03-03T15:03:31.309896-07:00",
        "id": "412be771-19bf-4452-9e84-549a52916951"
    }
]
        }
    )}


ObjectsLikedGet = {
    200: openapi.Response(
        description='Sucessfully retrieve Liked objects',
        examples={'application/json': {
  "type": "liked",
  "items": [
    {
      "summary": "TomHardyUpdated Likes your post",
      "type": "Like",
      "author": {
        "type": "author",
        "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "host": "",
        "displayName": "TomHardyUpdated",
        "github": "",
        "profileImage": ""
      },
      "object": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561"
    }
  ]
}}
    )
}

PostsGet = {
    "200": openapi.Response(
        description="Successfully retrieved posts",
        examples={
            "application/json": {
  "count": 1,
  "next": 'null',
  "previous": 'null',
  "results": [
    {
      "type": "post",
      "title": "Testing",
      "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561",
      "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561",
      "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561",
      "description": "Good",
      "contentType": "text/plain",
      "content": "Yes",
      "author": {
        "type": "author",
        "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
        "host": "",
        "displayName": "TomHardyUpdated",
        "github": "",
        "profileImage": ""
      },
      "categories": [
        "Hi"
      ],
      "count": 0,
      "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561/comments/",
      "commentsSrc": [],
      "published": "2023-03-23T15:18:18.709951-07:00",
      "visibility": "PUBLIC"
    }
  ]
}
        }
    )}

PostsPOST = {
    "200": openapi.Response(
        description="Successfully created post",
        examples={
            "application/json": {
  "type": "post",
  "title": "test",
  "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "host": "",
    "displayName": "TomHardyUpdated",
    "github": "",
    "profileImage": ""
  },
  "categories": [
    ""
  ],
  "count": 0,
  "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece/comments/",
  "commentsSrc": [],
  "published": "2023-03-23T16:39:41.602108-07:00",
  "visibility": "PUBLIC"
}
        }
    )}

IndividualPOSTGet = {
    "200": openapi.Response(
        description="Successfully Retrieved individual post",
        examples={
            "application/json": {
  "type": "post",
  "title": "test",
  "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "host": "",
    "displayName": "TomHardyUpdated",
    "github": "",
    "profileImage": ""
  },
  "categories": [
    ""
  ],
  "count": 0,
  "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece/comments/",
  "commentsSrc": [],
  "published": "2023-03-23T16:39:41.602108-07:00",
  "visibility": "PUBLIC"
}
        }
    )}

IndividualPOSTPost = {
    "200": openapi.Response(
        description="Successfully Updated individual post",
        examples={
            "application/json": {
  "type": "post",
  "title": "Updated POST!!!",
  "id": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "source": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "origin": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
    "host": "",
    "displayName": "TomHardyUpdated",
    "github": "",
    "profileImage": ""
  },
  "categories": [
    ""
  ],
  "count": 0,
  "comments": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/02fdf43f-294a-45ff-8df4-4516b9869ece/comments/",
  "commentsSrc": [],
  "published": "2023-03-23T16:39:41.602108-07:00",
  "visibility": "PUBLIC"
}
        }
    )}

CreateComment = {
    "200": openapi.Response(
        description="Successfully Created comment",
        examples={
            "application/json": {
  "type": "comment",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "host": "",
    "displayName": "LaraCroft",
    "github": "",
    "profileImage": ""
  },
  "comment": "hi",
  "contentType": "text/plain",
  "published": "2023-03-23T17:04:10.945180-07:00",
  "id": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
}
        }
    )}


GetComments = {
    "200": openapi.Response(
        description="Successfully Retrieve comment",
        examples={
            "application/json": {
  "count": 1,
  "next": 'null',
  "previous": 'null',
  "results": [
    {
      "type": "comment",
      "author": {
        "type": "author",
        "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
        "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
        "host": "",
        "displayName": "LaraCroft",
        "github": "",
        "profileImage": ""
      },
      "comment": "hi",
      "contentType": "text/plain",
      "published": "2023-03-23T17:04:10.945180-07:00",
      "id": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
    }
  ]
}
        }
    )}


GetCommentLikes =  {
    "200": openapi.Response(
        description="Successfully Retrieve comment likes",
        examples={
            "application/json": [
  {
    "summary": "TomHardyUpdated Likes your comment",
    "type": "Like",
    "author": {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "host": "",
      "displayName": "TomHardyUpdated",
      "github": "",
      "profileImage": ""
    },
    "object": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
  }
]
        }
    )}




GetInvdividualComment = {
    "200": openapi.Response(
        description="Successfully Retrieved comments",
        examples={
            "application/json": {
  "type": "comment",
  "author": {
    "type": "author",
    "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
    "host": "",
    "displayName": "LaraCroft",
    "github": "",
    "profileImage": ""
  },
  "comment": "hi",
  "contentType": "text/plain",
  "published": "2023-03-23T17:04:10.945180-07:00",
  "id": "http://127.0.0.1:8000/posts/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6/posts/2aa56a61-85df-4dee-8b00-7c2cabf2b161/comments/c5c03638-47ce-412f-b23c-d785c2ea7525"
}
        }
    )}


PostLikes = {
    "200": openapi.Response(
        description="Successfully Retrieved Likes on a post",
        examples={
            "application/json": [
  {
    "summary": "LaraCroft Likes your post",
    "type": "Like",
    "author": {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "url": "http://127.0.0.1:8000/authors/cfd9d228-44df-4a95-836f-c0cb050c7ad6",
      "host": "",
      "displayName": "LaraCroft",
      "github": "",
      "profileImage": ""
    },
    "object": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561"
  },
  {
    "summary": "TomHardyUpdated Likes your post",
    "type": "Like",
    "author": {
      "type": "author",
      "id": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "url": "http://127.0.0.1:8000/authors/971fa387-b101-4276-891f-d970f2cf0cad",
      "host": "",
      "displayName": "TomHardyUpdated",
      "github": "",
      "profileImage": ""
    },
    "object": "http://127.0.0.1:8000/posts/authors/971fa387-b101-4276-891f-d970f2cf0cad/posts/c62938df-7b80-481a-bfda-07e768df6561"
  }
]
        }

    )}


class post_list(APIView, PageNumberPagination):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # for pagination
    serializer_class = PostSerializer
    pagination_class = PostSetPagination
    

    # TODO: RESPONSE AND REQUESTS
    
    @swagger_auto_schema(responses =PostsGet, operation_summary="List all Posts for an Author")
    def get(self, request, pk_a):
        """
        Get the list of posts on our website
        """
        author = Author.objects.get(id=pk_a)
        posts = Post.objects.filter(author=author)
        posts = self.paginate_queryset(posts, request)
        #authenticated_user = Author.objects.get(id=pk_a)

        # for post in posts:
        #     if "PRIVATE" in post.visibility:
        #         # if the post author is not the auth'd user, don't show this post
        #         if post.author != authenticated_user:
        #             posts.exclude(post)
                    
        #     if "FRIENDS" in post.visibility:
        #         # if the post author is not friends with the auth'd user, don't show this post
        #         if authenticated_user not in post.author.friends or authenticated_user != post.author:
        #             posts.exclude(post)
                
        #     if "UNLISTED" in post.visibility:
        #         # if the post is marked as unlisted, don't show this post UNLESS the author is the one authenticated
        #         # (other users can see it if they have the link)
        #         if post.author != authenticated_user:
        #             posts.exclude(post)
        
        posts = self.paginate_queryset(posts, request) 
        # if authenticated_user not in post.author.friends:
        #     posts.exclude(post) 

        serializer = PostSerializer(posts, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(responses = PostsPOST, operation_summary="Create a new Post for an Author",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the POST request',example = {
     "type":"post",
     "title":"test",
     "description":"testing testy test",
     "contentType":"text/plain",
     "content":"test"
}))
    def post(self, request, pk_a):
        """
        New post for an Author
        Request: include mandatory fields of a post, not including author, id, origin, source, type, count, comments, commentsSrc, published
        """
        pk = str(uuid.uuid4())
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        # if image post
        if 'image' in request.data['contentType']:
            serializer = ImageSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})
            # you will need to pass in a JSON object with a title, contentType, content, and image
            # image is passed in as a base64 string. it should look like data:image/png;base64,LOTSOFLETTERS
        else:
            serializer = PostSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})

        if serializer.is_valid():
            post = serializer.save()
            share_object(post,author)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]    
    @swagger_auto_schema(responses = GetInvdividualComment, operation_summary="List specific comment")
    def get(self, request, pk_a, pk, pk_m):
        """
        Get the specific comment
        """
        try: 
            comment = Comment.objects.get(id=pk_m)
            serializer = CommentSerializer(comment, many=False)
            return Response(serializer.data)
        except Comment.DoesNotExist: 
            error_msg = "Comment not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
class post_detail(APIView, PageNumberPagination):
    serializer_class = PostSerializer
    pagination_class = PostSetPagination

    @swagger_auto_schema(responses = IndividualPOSTGet, operation_summary="Get a particular post of an author")
    def get(self, request, pk_a, pk):
        """
        Get a particular post of an author
        """
        try: 
            post = Post.objects.get(id = pk)
            authenticated_user = Author.objects.get(id=pk_a)

            # unlisted does not need to be addressed here; only in the post list
            # if it is private or friends, only continue if author is trying to access it:
            if "PRIVATE" in post.visibility:
                # check if the author is not the one accessing it:
                # TODO: specifically shared users
                if post.author != authenticated_user:
                    error_msg = {"message":"You do not have access to this post!"}
                    return Response(error_msg,status=status.HTTP_403_FORBIDDEN)

            # otherwise, handle it for friends:
            if "FRIENDS" in post.visibility:
                # if the author or friends are trying to access it:
                if post.author not in authenticated_user.friends and post.author != authenticated_user:
                    error_msg = {"message":"You do not have access to this post!"}
                    return Response(error_msg,status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist: 
            error_msg = "Comment not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    #content for creating a new post object
    #{
    # Title, Description, Content type, Content, Categories, Visibility
    # }
    @swagger_auto_schema(responses = IndividualPOSTPost, operation_summary="Update a particular post of an author",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the POST request',example = {"title":"Updated POST!!!"}))
    def post(self, request, pk_a, pk):       
        """
        Request: only include fields you want to update, not including id or author.
        """     
        try:
            _ = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            error_msg = "Post not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        # TODO: FIX AFTER SLASH
        if post.url == post.origin:
            if post.author != _:
                return Response("Cannot edit a post you didnt create", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            if 'image' in request.data['contentType']:
                serializer = ImageSerializer(data=request.data, context={'author_id': pk_a})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else: 
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else: 
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response("Cannot edit a shared post", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete a particular post of an author") 
    def delete(self, request, pk_a, pk):
        """
        Deletes the post given by the particular authorid and postid
        """
        # TODO: check permissions 
        try: 
            try:
                author = Author.objects.get(id=pk_a)
            except:
                error_msg = "Author not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
            post = Post.objects.get(id=pk)
            if post.author != author:
                return Response("Cannot delete a post you dont own", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response("Post does not exist",status=status.HTTP_404_NOT_FOUND)
      

    @swagger_auto_schema(responses =PostsPOST, operation_summary="Create a post of an author whose id is the specified post id",request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the PUT request',example = {
  "type": "post",
  "title": "test2",
  "description": "testing testy test",
  "contentType": "text/plain",
  "content": "test"
})) 
    def put(self, request, pk_a, pk):
        """
        Request: include mandatory fields of a post, not including author, id, origin, source, type, count, comments, commentsSrc, published
        """
        try:
            author = Author.objects.get(id=pk_a)
            try:
                _ = Post.objects.get(id=pk)
                return Response("Post already exists", status=status.HTTP_400_BAD_REQUEST)
            except Post.DoesNotExist:
                pass
        except Author.DoesNotExist:
            Response("Author does not exist", status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})
        if serializer.is_valid():
            post = serializer.save()
            share_object(post,author)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikedView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # TODO: RESPONSE AND REQUESTS
    
    @swagger_auto_schema(responses = ObjectsLikedGet, operation_summary="List all objects liked by author")
    def get(self, request, pk_a):
        """
        Get the liked objects by author
        TODO: make sure objects are public
        """
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author not found"
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        likes = Like.objects.filter(author=author)
        serializer = LikeSerializer(likes, many=True)
        data = self.get_items(pk_a, serializer.data)
        return Response(data)
    
    def get_items(self,pk_a,data):
        # helper function 
        
        dict = {"type":"liked" }
        items = []
        for item in data:
            items.append(item)

        dict["items"] = items
        return(dict) 
    
class CommentLikesView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """
    Get the list of likes on our comments
    """
    @swagger_auto_schema(responses=GetCommentLikes,operation_summary="List all likes on a comment")
    def get(self, request, pk_a, pk, pk_m):
        try:
            comment = Comment.objects.get(id=pk_m)
        except Author.DoesNotExist:
            error_msg = "Comment not found"
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        likes = Like.objects.filter(object=comment.url)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

@swagger_auto_schema( method='get', operation_summary="Get the comments on a post")
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_comments(request, pk_a, pk):
    """
    Get the list of comments on the post
    """
    author = Author.objects.get(id=pk_a)
    post = Post.objects.get(author=author, id=pk)
    comments = Comment.objects.filter(author=author,post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

class PostLikesView(APIView):

    @swagger_auto_schema(operation_summary="Get the likes on a post")
    @authentication_classes([BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def get(request, pk_a):
        """
        Get the list of likes on a post
        """
        post = Post.objects.get(id=request[""])
        likes = Like.objects.filter(object=post.url)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

# hari, I assumed that authenticated_user is an author object
class ImageView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a) 
            post = Post.objects.get(author=author, id=pk)
            authenticated_user = Author.objects.get(id=pk_a)

            # not image post
            if post.contentType and 'image' not in post.contentType:
                error_msg = {"message":"Post does not contain an image!"}
                return Response(error_msg,status=status.HTTP_404_NOT_FOUND)

            # no image included in post
            if not post.image:
                error_msg = {"message":"Post does not contain an image!"}
                return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
            
            # image privacy settings
            # unlisted does not need to be addressed here
            # if it is private or friends, only continue if author is trying to access it:
            if "PRIVATE" in post.visibility:
                # check if the author is not the one accessing it:
                if post.author != authenticated_user:
                    error_msg = {"message":"You do not have access to this image!"}
                    return Response(error_msg,status=status.HTTP_403_FORBIDDEN)

            # otherwise, handle it for friends:
            elif "FRIENDS" in post.visibility:
                # if the author or friends are trying to access it:
                # this line will likely be bugged until auth is set up ┐(´～｀)┌
                if post.author not in authenticated_user.friends and post.author != authenticated_user:
                    error_msg = {"message":"You do not have access to this image!"}
                    return Response(error_msg,status=status.HTTP_403_FORBIDDEN)

            # return the image!
            post_content = post.contentType.split(';')[0]
            return Response(post.image, content_type=post_content, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            error_msg = {"message":"Post does not exist!"}
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        
# hari, this is another section which takes in the authed user as an author.
class CommentView(APIView, PageNumberPagination):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = PostSetPagination
    page_size_query_param = 'page_size'

    
    @swagger_auto_schema(responses =GetComments, operation_summary="List all Comments on a post")
    def get(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        post = Post.objects.get(id=pk)
        # changed to filter for all comments on the post, it was filtering
        # the comments by the author of the post on the post otherwise.
        # comments = Comment.objects.filter(author=author,post=post)
        comments = Comment.objects.filter(post=post)

        # just change this to whoever is authed
        authenticated_user = Author.objects.get(id=pk_a)
        
        # on private posts, friends' comments will only be available to me.
        if "PRIVATE" in post.visibility:
            # so here, when authed user != author, the comments of the friends
            # of the author are filtered out
            if post.author != authenticated_user:
                comments = comments.exclude(author=post.author.friends)
        
        paginator = self.pagination_class()
        comments_page = paginator.paginate_queryset(comments, request, view=self)
        serializer = CommentSerializer(comments_page, many=True)
        commentsObj = {}
        commentsObj['comments'] = serializer.data
        response = paginator.get_paginated_response(serializer.data)
        return response


    @swagger_auto_schema(responses =CreateComment, operation_summary="Create a comment on the post", request_body=openapi.Schema( type=openapi.TYPE_STRING,description='A raw text input for the PUT request', example = {"author_id" : "cfd9d228-44df-4a95-836f-c0cb050c7ad6", "comment": "hi"}))
    def post(self, request,pk_a, pk):
        comment_id = uuid.uuid4()
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        try: 
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            error_msg = "Post id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(data=request.data, context={"post":post,"id":comment_id, 'author_id':request.data["author_id"]}, partial=True)
        if serializer.is_valid():
            comment = serializer.save()
            inbox_item = Inbox(content_object=comment, author=post.author)
            inbox_item.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# post to url 'authors/<str:origin_author>/posts/<str:post_id>/share/<str:author>'

class ShareView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, origin_author, post_id, author):       
        
        try:
            sharing_author = Author.objects.get(pk=author)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            error_msg = "Post id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        

        # create new post object with different author but same origin
        #new URL 
        current_url = post.get_absolute_url()
        source = current_url.split('share')[0]
        origin = post.origin
        
        new_post = Post(
        title=post.title,
        description=post.description,
        content=post.content,
        contentType=post.contentType,
        author=sharing_author,
        categories=post.categories,
        published=post.published,
        visibility=post.visibility,
        )

        # update the source and origin fields
        new_post.source = source
        new_post.origin = origin

        # save the new post
        new_post.save()
        share_object(new_post,sharing_author)
        serializer = PostSerializer(new_post)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicPostsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(visibility='PUBLIC')
        serializer = PostSerializer(posts, many=True)
        data_list = serializer.data

        yoshi = getNodeAuthors_Yoshi()
        
        for yoshi_author in yoshi:
            id = yoshi_author["id"].split('/')[-1] or yoshi_author["id"]
            posts = getNodePost_Yoshi(id)
            posts = posts[0]['items']
            for post in posts:
                if post["visibility"]=='Public':
                    data_list.append(post)
        social_distro = getNodeAuthors_social_distro()
        for social_distro_author in social_distro:
            id = social_distro_author["id"].split('/')[-1] or social_distro_author["id"]
            posts = getNodePost_social_distro(id)
            
            posts = posts['results']
            print(posts)
            for post in posts:
                if post["visibility"]=='PUBLIC':
                    data_list.append(post)
        return Response(data_list)
        
def share_object(item, author):
    inbox_item = Inbox(content_object=item, author=author)
    inbox_item.save()

    if (item.visibility == 'FRIENDS'):
        for friend in author.friends.all():
            inbox_item = Inbox(content_object=item, author=friend)
            inbox_item.save()

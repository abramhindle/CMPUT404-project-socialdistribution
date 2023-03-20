from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from django.views import generic
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.http import HttpResponse
from rest_framework.decorators import api_view
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
from .image_renderer import JPEGRenderer, PNGRenderer

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

class post_list(APIView, PageNumberPagination):

    # for pagination
    serializer_class = PostSerializer
    pagination_class = PostSetPagination
    

    # TODO: RESPONSE AND REQUESTS
    
    @swagger_auto_schema(responses=response_schema_dictposts,operation_summary="List all Posts for an Author")
    def get(self, request, pk_a):
        """
        Get the list of posts on our website
        """
        author = Author.objects.get(id=pk_a)
        posts = Post.objects.filter(author=author)
        authenticated_user = Author.objects.get(id=pk_a)

        for post in posts:
            if "PRIVATE" in post.visibility:
                # if the post author is not the auth'd user, don't show this post
                if post.author != authenticated_user:
                    posts.exclude(post)
                    
            if "FRIENDS" in post.visibility:
                # if the post author is not friends with the auth'd user, don't show this post
                if authenticated_user not in post.author.friends:
                    posts.exclude(post)
        
        posts = self.paginate_queryset(posts, request) 
        serializer = PostSerializer(posts, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(responses=response_schema_dictposts,operation_summary="Create a new Post for an Author")

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
        
        serializer = PostSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})
        if serializer.is_valid():
            post = serializer.save()
            inbox_item = Inbox(content_object=post, author=author)
            for friend in author.friends.all():
                inbox_item = Inbox(content_object=post, author=friend)
            inbox_item.save()
            for friend in author.friends.all():
                inbox_item = Inbox(content_object=post, author=friend)
                inbox_item.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView, PageNumberPagination):
    
    @swagger_auto_schema(responses=response_schema_dictposts,operation_summary="List specific comment")
    def get(self, request, pk_a, pk, pk_m):
        """
        Get the specific comment
        """
        # ERROR HERE
        try: 
            comment = Comment.objects.filter(id=pk_m)
            comment = self.paginate_queryset(comment, request) 
            serializer = CommentSerializer(comment, many=True)
            return self.get_paginated_response(serializer.data)
        except Comment.DoesNotExist: 
            return self.put(request, pk_a, pk)
        
class post_detail(APIView, PageNumberPagination):
    serializer_class = PostSerializer
    pagination_class = PostSetPagination

    @swagger_auto_schema(responses=response_schema_dictpost,operation_summary="Get a particular post of an author")
    def get(self, request, pk_a, pk):
        """
        Get a particular post of an author
        """
        try: 
            post = Post.objects.get(id = pk)
            authenticated_user = Author.objects.get(id=pk_a)

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
                    error_msg = {"message":"You do not have access to this image!"}
                    return Response(error_msg,status=status.HTTP_403_FORBIDDEN)
                
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data)
        except Post.DoesNotExist: 
            error_msg = "Comment not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
    
    #content for creating a new post object
    #{
    # Title, Description, Content type, Content, Categories, Visibility
    # }
    @swagger_auto_schema(responses=response_schema_dictpost,operation_summary="Update a particular post of an author") 
    def post(self, request, pk_a, pk):       
        """
        Request: only include fields you want to update, not including id or author.
        """     
        print("hello1") 
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
        
        # if image post
        if 'image' in request.data['contentType']:
            serializer = ImageSerializer(data=request.data, context={'author_id': pk_a})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else: 
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            
        serializer = PostSerializer(post, data=request.data, partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses=response_schema_dictdelete,operation_summary="Delete a particular post of an author") 
    def delete(self, request, pk_a, pk):
        """
        Deletes the post given by the particular authorid and postid
        """
        # TODO: check permissions 

        try: 
            post = Post.objects.filter(id=pk)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response("Post does not exist",status=status.HTTP_404_NOT_FOUND)
      

    @swagger_auto_schema(responses=response_schema_dictpost,operation_summary="Create a post of an author whose id is the specified post id") 
    def put(self, request, pk_a, pk):
        """
        Request: include mandatory fields of a post, not including author, id, origin, source, type, count, comments, commentsSrc, published
        """
        try:
            _ = Author.objects.get(id=pk_a)
            try:
                _ = Post.objects.get(id=pk)
                return Response("Post already exists", status=status.HTTP_400_BAD_REQUEST)
            except Post.DoesNotExist:
                pass
        except Author.DoesNotExist:
            Response("Author does not exist", status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data, context={'author_id': pk_a, 'id':pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikedView(APIView):

    # TODO: RESPONSE AND REQUESTS
    
    @swagger_auto_schema(responses=response_schema_dictposts,operation_summary="List all objects liked by author")
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

@swagger_auto_schema( method='get',responses=response_schema_dictComments,operation_summary="Get the comments on a post")
@api_view(['GET'])
def get_comments(request, pk_a, pk):
    """
    Get the list of comments on our website
    """
    author = Author.objects.get(id=pk_a)
    post = Post.objects.get(author=author, id=pk)
    comments = Comment.objects.filter(author=author,post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@swagger_auto_schema( method='get',responses=response_schema_dictpost,operation_summary="Get a partdsfdidsf of an author")
@api_view(['GET'])
def get_likes(request, pk_a, pk):
    """
    Get the list of comments on our website
    """
    post = Post.objects.get(id=pk)
    likes = Like.objects.filter(object=post.id)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

class ImageView(APIView):
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
            # if it is private or friends, only continue if author is trying to access it:
            if "PRIVATE" in post.visibility:
                # check if the author is not the one accessing it:
                if post.author != authenticated_user:
                    error_msg = {"message":"You do not have access to this image!"}
                    return Response(error_msg,status=status.HTTP_403_FORBIDDEN)

            # otherwise, handle it for friends:
            if "FRIENDS" in post.visibility:
                # if the author or friends are trying to access it:
                if post.author not in authenticated_user.friends and post.author != authenticated_user:
                    error_msg = {"message":"You do not have access to this image!"}
                    return Response(error_msg,status=status.HTTP_403_FORBIDDEN)
            
            # return the image!
            post_content = post.contentType.split(';')[0]
            return Response(post.image, content_type=post_content, status=status.HTTP_200_OK)

        # but it's not real!
        except Post.DoesNotExist:
            error_msg = {"message":"Post does not exist!"}
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        

        # like_id = uuid.uuid4()
        # # url = request.data
        # # url 
        # post_url = request.data['object']
        # author = request.data['author']
        # try:
        #     author = Author.objects.get(pk=pk_a)
        # except Author.DoesNotExist:
        #     error_msg = "Author id not found"
        #     return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        # try: 
        #     #setup the URL and check to see if it exists already
        #     #like = Like.object.get(author = pk_a, object = url)
        #     like = Like.objects.get(auhtor=author, object=post_url )
        #     return Response('Already Liked')
        # except Like.DoesNotExist:
        #      #find a way to get inbox of author and put inbox into data that goes in serializer
        #     try:
        #         inbox = Inbox.object.get(author=author)
        #     except Inbox.DoesNotExist:
        #         return Response("Inbox does not exist", status=status.HTTP_400_BAD_REQUEST)
        #     all_data = request.data
        #     all_data['inbox'] = inbox 
        #     serializer = LikeSerializer(data=all_data, context={'author_id': pk_a})
        #     if serializer.is_valid():
        #         serializer.validated_data.pop("author")
        #         like = Like.objects.create(**serializer.validated_data, author=author, id=like_id, )
        #         like.update_fields_with_request(request)

        #         serializer = LikeSerializer(like, many=False)
        #         return Response(serializer.data)
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # # try:
        # #     author = Author.objects.get(id=pk_a)
        # # except Author.DoesNotExist:
        # #     return Response(status=status.HTTP_404_NOT_FOUND)
        
        # # data = {'author': author.id, **request.data}
        # # serializer = LikeSerializer(data=data)
        
        # # if serializer.is_valid():
        # #     serializer.save()
        # #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # # else:
        # #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# hari, this is another section which takes in the authed user as an author.
class CommentView(APIView, PageNumberPagination):
    serializer_class = CommentSerializer
    pagination_class = PostSetPagination

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
                
        serializer = CommentSerializer(comments, many=True)

        commentsObj = {}
        commentsObj['comments'] = serializer.data
        return Response(commentsObj)

    
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
        current_url = request.build_aboslute_url
        source = current_url.split('share')[0]
        origin = post.origin
        
        new_post = Post(
        title=post.title,
        description=post.description,
        content=post.content,
        contentType=post.contentType,
        author=post.author,
        categories=post.categories,
        published=post.published,
        visibility=post.visibility,
        )

        # update the source and origin fields
        new_post.source = source
        new_post.origin = origin

        # save the new post
        new_post.save()
        serializer = PostSerializer(new_post)
        return Response(serializer.data)
        

from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from django.views import generic
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from author.pagination import *
from posts.serializers import *
from .models import *
from .serializers import *
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

response_schema_dict = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": {
        "type": "author",
        "id": "866ff975-bb49-4c75-8cc8-10e2a6af44a0",
        "displayName": "Fahad",
        "url": "",
        "profileImage": ""
    }
        }
    )}

response_schema_dict = {
    "200": openapi.Response(
        description="Successful Operation",
        examples={
            "application/json": {
            "type": "inbox",
            "author": "http://127.0.0.1:8000/authors/a1",
            "items": [
                {
                    "type": "post",
                    "title": "A post title about a post about web dev",
                    "id": "http://127.0.0.1:8000/posts/authors/a2/posts/p2",
                    "source": "",
                    "origin": "",
                    "description": "This post discusses stuff -- brief",
                    "contentType": "text/plain",
                    "content": "Example content",
                    "author": {
                        "type": "author",
                        "id": "http://127.0.0.1:8000/authors/a2",
                        "displayName": "NewLeen",
                        "profileImage": ""
                    },
                    "categories": [
                        ""
                    ],
                    "comments": "http://127.0.0.1:8000/posts/authors/a2/posts/p2/comments/",
                    "published": "2023-03-07T14:07:52.316462-07:00",
                    "visibility": "PUBLIC"
                },
                ]
            }
        }
    )}


class AuthorsListView(APIView, PageNumberPagination):
    # for pagination
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100

    @swagger_auto_schema(responses=response_schema_dict,operation_summary="List of Authors registered")
    def get(self, request):
        
        """
        Get the list of authors on our website
        """
        authors = Author.objects.all()
        authors=self.paginate_queryset(authors, request) 
        serializer = AuthorSerializer(authors, many=True)
        return self.get_paginated_response(serializer.data)

class AuthorView(APIView):
    def validate(self, data):
        if 'displayName' not in data:
            data['displayName'] = Author.objects.get(displayName=data['displayName']).weight
        return data 

    @swagger_auto_schema(responses=response_schema_dict,operation_summary="Finds Author by iD")
    def get(self, request, pk_a):

        """
        Get a particular author searched by AuthorID
        """
        author = Author.objects.get(id=pk_a)
        serializer = AuthorSerializer(author,partial=True)
        return  Response(serializer.data)
    
    @swagger_auto_schema( responses=response_schema_dict,operation_summary="Update a particular Authors profile")
    def put(self, request, pk_a):
        """
        Update the authors profile
        """

        author = Author.objects.get(pk=pk_a)
           
        serializer = AuthorSerializer(author,data=request.data,partial=True)
         
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FollowersView(APIView):
    serializer_class = AuthorSerializer

    # The get function is called witha  get request. The function is called by using 
    # ://authors/authors/{AUTHOR_ID}/followers/ to get a list of followers
    # or call using ://authors/authors/{AUTHOR_ID}/followers/foreign_author_id/ to check if foriegn author is following author
    #Implement later after talking to group 
    # @swagger_auto_schema(method ='get',responses=response_schema_dict,operation_summary="List of Followers")
    def get(self, request, pk_a, pk=None):
        try:
            author = Author.objects.get(id=pk_a)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        # If url is /authors/authors/author_id/followers/
        if pk ==None:
            followers = author.friends.all()
            followers_list = []
            for follower in followers:
                try: 
                    follower_author = Author.objects.get(id=follower.id)
                except Author.DoesNotExist:
                    error_msg = "Follower id not found"
                    return Response(error_msg, status=status.HTTP_404_NOT_FOUND) 
                followers_list.append(follower_author.follower_to_object())

            results = {"type": "followers",
                    "items": followers_list
            }

            return Response(results, status=200)
        # else If url is /authors/authors/author_id/followers/foreign_author_id    
        else:
            try:
                follower = Author.objects.get(id=pk)
            # follower = Author.objects.get(id=request.data["foreign_author_id"])
            except Author.DoesNotExist:
                error_msg = "Foreign Author id not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

            friends = author.friends.all()
            if follower in friends:
                serializer = AuthorSerializer(follower,partial=True)
                #returns the follower
                return  Response(serializer.data)
            else:
                #if the follower is not apart of the followers lis return empty{}
                return Response({})
            

    #For this we need nothing in the content field only the url with the author id of the person that is being followed by foreign author id 
    #call using ://authors/authors/{AUTHOR_ID}/followers/foreign_author_id/
    #Implement later after talking to group 
    # @swagger_auto_schema(method ='get',responses=response_schema_dict,operation_summary="New Follower")
    def put(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        try:
            new_follower = Author.objects.get(id=pk)
            # new_follower = Author.objects.get(id=request.data["foreign_author_id"])
        except Author.DoesNotExist:
            error_msg = "Follower id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        followers = author.friends
        followers.add(new_follower)
        print("ayo")
        author.save()
        try: 
            follow = FollowRequest.objects.get(actor=new_follower,object=author)
            Inbox.objects.get(object_id=follow.id).delete()
        except:
            pass

        followers = author.friends.all()
        followers_list = []
        for follower in followers:
            try: 
                follower_author = Author.objects.get(id=follower.id)
            except Author.DoesNotExist:
                error_msg = "Follower id not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND) 
            followers_list.append(follower_author.follower_to_object())

        # return the new list of followers
        return Response(followers_list)

    #For the delete request we need nothing in the content field only the url with the author id of the person that is being followed by foreign author id
    #Implement later after talking to group 
    # @swagger_auto_schema(method ='get',responses=response_schema_dict,operation_summary="Delete Follower")
    def delete(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a)
            # author = Author.objects.get(id=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        try:
            removed_follower = Author.objects.get(id=pk)
            # removed_follower = Author.objects.get(id=request.data["foreign_author_id"])
        except Author.DoesNotExist:
            error_msg = "Follower id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        followers = author.friends
        followers.remove(removed_follower)
        author.save()

        followers = author.friends.all()
        followers_list = []
        for follower in followers:
            try: 
                follower_author = Author.objects.get(id=follower.id)
            except Author.DoesNotExist:
                error_msg = "Follower id not found"
                return Response(error_msg, status=status.HTTP_404_NOT_FOUND) 
            followers_list.append(follower_author.follower_to_object())
        
        # return the new list of followers
        return Response(followers_list)

class FriendRequestView(APIView):
    serializer_class = FollowRequestSerializer
    
    def post(self,request,pk_a):
        actor = Author.objects.get(id=pk_a)
        displaynameto = request.data['displayName']
        displaynamefrom=actor.displayName
        objects = Author.objects.filter(displayName = displaynameto)[0]

        if FollowRequest.objects.filter(actor=actor, object=objects).exists():
            return Response("You've already sent a request to this user", status=status.HTTP_400_BAD_REQUEST)
        if actor==objects:
            return Response("You cannot follow yourself!", status=status.HTTP_400_BAD_REQUEST)
        
        type = "Follow"
        summary = displaynamefrom + " wants to follow " + displaynameto
        follow = FollowRequest(Type = type,Summary=summary,actor=actor, object=objects)
        follow.save()
        serializer = FollowRequestSerializer(follow)
        return Response(serializer.data)
    
class ViewRequests(APIView):
    serializer_class = FollowRequestSerializer
    # @permission_classes([IsAuthenticated])
    def get(self,request,pk_a):
        """
        Get the list of Follow requests for the current Author
        """

        Object = Author.objects.get(id=pk_a)
        displaynamefrom=Object.displayName

        requests = FollowRequest.objects.filter(object = Object)
        serializer = FollowRequestSerializer(requests,many=True)
        return Response(serializer.data)

class InboxSerializerObjects:
    def serialize_inbox_objects(self, item, context={}):
        # return the serializer data of all objects in inbox
        object_model = item.content_type.model_class()
        if object_model is Post:
            serializer = PostSerializer
        elif object_model is Like:
            serializer = LikeSerializer
        elif object_model is Comment:
            serializer = CommentSerializer
        elif object_model is FollowRequest:
            serializer = FollowRequestSerializer
        return serializer(item.content_object, context=context).data
    
    def deserialize_objects(self, data, pk_a):
        # return serializer of objects to be added to inbox (so we get the object)
        type = data.get('type')
        obj = None
        if type is None:
            raise exceptions
        
        if type == Post.get_api_type():
            obj = Post.objects.get(id=(data["id"].split("/")[-1]))
            serializer = PostSerializer
            context={'author_id': pk_a,'id':data["id"].split("/")[-1]}
        elif type == Like.get_api_type():
            # TODO: Add a check to see if the author liked that object before, then just return obj
            serializer = LikeSerializer
            context={'author_id': data["author_id"]}
        elif type == Comment.get_api_type():
            serializer = CommentSerializer
            context={'author_id': pk_a,'id':data["id"].split("/")[-1]}
        elif type == FollowRequest.get_api_type():
            serializer = FollowRequestSerializer
            context={'actorr': data["actor"]["id"],'objectt':data["object"]["id"]}
            
         
      
        return obj or serializer(data=data, context=context, partial=True)

class Inbox_list(APIView, InboxSerializerObjects, PageNumberPagination):
    """
        URL: author/auhor_id/inbox
    """

    serializer_class = InboxSerializer
    pagination_class = InboxSetPagination

    @swagger_auto_schema( responses=response_schema_dict,operation_summary="Get all the objects in the inbox")
    def get(self, request, pk_a):
        # GET all objects in inbox, only need auth in request

        author = get_object_or_404(Author,pk=pk_a)
        inbox_data = author.inbox.all()
        inbox_data = self.paginate_queryset(inbox_data,request)
        serializer = InboxSerializer(data=inbox_data, context = {"serializer":self.serialize_inbox_objects}, many=True)
        serializer.is_valid()
        data = self.get_items(pk_a, serializer.data)
        # TODO: Fix pagination
        return self.get_paginated_response(data)
    
    @swagger_auto_schema( responses=response_schema_dict,operation_summary="Post a new object to the inbox")
    def post(self, request, pk_a):
        """
            POST a new object to inbox
            request: 
            1. If the object is from a foreign author and not in database: a full object (Like, Author, Comment) with mandatory fields required, TYPE, id, author.
            2. If object in database: TYPE, id.
        """
        author = get_object_or_404(Author,pk=pk_a)
        serializer = self.deserialize_objects(
            self.request.data, pk_a)
        
        # Case 1: friend author is outside the server, we create all these objects in our database (not sure)
        try:
            if serializer.is_valid():
                item = serializer.save()
                if item=="already liked":
                    return Response("Post Already Liked!")
                if item == "already sent":
                    return Response("You've already sent a request to this user!")
                if item == "same":
                    return Response("You cannot send a follow request to yourself!")
                if hasattr(item, 'update_fields_with_request'):
                    item.update_fields_with_request(request)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Case 2: author is within the server
        except AttributeError as e:
            item = serializer   
        inbox_item = Inbox(content_object=item, author=author)
        inbox_item.save()
        return Response({'request': self.request.data, 'saved': model_to_dict(inbox_item)})
    
    
    @swagger_auto_schema( responses=response_schema_dict,operation_summary="Delete all the objects in the inbox")
    def delete(self, request, pk_a):
        # GET all objects in inbox, only need auth in request
        try: 
            author = get_object_or_404(Author,pk=pk_a)
            author.inbox.all().delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response("Post does not exist",status=status.HTTP_404_NOT_FOUND)
    
    
    def get_items(self,pk_a,data):
        # helper function 
        
        dict = {"type":"inbox", "author": settings.APP_NAME + '/authors/' + pk_a }
        items = []
        for item in data:
            items.append(item["content_object"])

        dict["items"] = items
        return(dict) 

@api_view(['GET'])
def getAuthor(request, displayName):
    """
    Get the list of comments on our website
    """
    author = Author.objects.get(displayName=displayName)
    serializer = AuthorSerializer(author,partial=True)
    return Response(serializer.data)
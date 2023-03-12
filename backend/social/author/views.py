from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from django.views import generic
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from author.pagination import InboxSetPagination
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
@swagger_auto_schema(method ='get',responses=response_schema_dict,operation_summary="List of Authors registered")
@api_view(['GET'])

def get_authors(request):
    """
    Get the list of authors on our website
    """
    authors = Author.objects
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


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
        author_id = pk_a 
           
        serializer = AuthorSerializer(data=request.data,partial=True)
         
        if serializer.is_valid():
            display = Author.objects.filter(id=author_id).values('displayName')
            if request.data['displayName'] == '':
                request.data._mutable = True
                request.data['displayName'] = display
            
            Author.objects.filter(id=author_id).update(**serializer.validated_data)
            author = Author.objects.get(id=pk_a)
            serializer = AuthorSerializer(author,partial=True)
            auth,created = Author.objects.update(**serializer.validated_data, id=author_id)
            
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
                    print (follower_author)
                except Author.DoesNotExist:
                    error_msg = "Follower id not found"
                    return Response(error_msg, status=status.HTTP_404_NOT_FOUND) 
                followers_list.append(follower_author.follower_to_object())

            # print(followers_list)
            return Response(followers_list)
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
        displaynameto = request.data['object.displayName']
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
    @permission_classes([IsAuthenticated])
    def get(self,request,pk_a):
        """
        Get the list of Follow requests for the current Author
        """

        Object = Author.objects.get(id=pk_a)
        displaynamefrom=Object.displayName
        print(53646456456456)
        print(FollowRequest.objects.filter(object = Object))

        requests = FollowRequest.objects.filter(object = Object)
        serializer = FollowRequestSerializer(requests,many=True)
        return Response(serializer.data)



class InboxSerializerObjects:
    def deserialize_inbox_objects(self, item, context={}):
        object_model = item.content_type.model_class()
        print("CONTENT",item.content_object)
        if object_model is Post:
            serializer = PostSerializer
        elif object_model is Like:
            serializer = LikeSerializer
        elif object_model is Comment:
            serializer = CommentSerializer
        return serializer(item.content_object, context=context).data
    
    def serialize_inbox_objects(self, data, pk_a):
        ## TODO: Make it clearner, use object_model = item.content_type.model_class()

        type = data.get('type')
        obj = None
        if type is None:
            raise exceptions
        context={'author_id': pk_a,'id':data["id"].split("/")[-1]}
        if type == Post.get_api_type():
            #print(data["id"].split("/")[-1])
            obj = Post.objects.get(id=(data["id"].split("/")[-1]))
            serializer = PostSerializer
        elif type == Like.get_api_type():
            obj = Like.objects.get(id=data["id"].split("/")[-1])
            serializer = LikeSerializer
        elif type == Comment.get_api_type():
            serializer = CommentSerializer
        if obj: return obj
        return serializer(data=data, context=context)

class Inbox_list(APIView, InboxSerializerObjects, PageNumberPagination):
    serializer_class = InboxSerializer
    pagination_class = InboxSetPagination

    def get(self, request, pk_a):
        author = get_object_or_404(Author,pk=pk_a)
        inbox_data = author.inbox.all()
        # Query Sey of inbox objects: [{'id': 'inbox id', 'author_id': 'author id', 'content_type_id': 1, 'object_id': '4cf1fb31-cc70-469c-97ff-4a6a28e483a8'}]
        print("DATA HERE",inbox_data.values())
        serializer = InboxSerializer(data=inbox_data, context={'author':author, 'serializer':self.deserialize_inbox_objects}, many=False)
        print("SERIALIZER HERE",serializer)
        serializer.is_valid()
        #serializer.save()
        return Response(serializer.data)
        
        return Response("No posts", status=status.HTTP_404_NOT_FOUND)
        paginated_inbox_data = self.paginate_queryset(inbox_data, request)
        return self.get_paginated_response([self.deserialize_inbox_objects(obj) for obj in paginated_inbox_data])
        return
    
    def post(self, request, pk_a):
        # author id is the id of the person who this notification comes from
        creator_id = request.data["author"]["id"].split("/")[-1]
        # print("creator", creator_id)
        author = Author.objects.get(pk=pk_a)
        serializer = self.serialize_inbox_objects(
            self.request.data, pk_a)
        try:
            if serializer.is_valid():
                item = serializer.save()
                if hasattr(item, 'update_fields_with_request'):
                    item.update_fields_with_request(request)
                inbox_item = Inbox(content_object=item, author=author)
                inbox_item.save()
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            item = serializer   
            inbox_item = Inbox(content_object=item, author = author)
            inbox_item.save()
        return Response({'req': self.request.data, 'saved': model_to_dict(inbox_item)})



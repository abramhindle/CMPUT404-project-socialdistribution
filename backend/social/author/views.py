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
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



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
            #auth,created = Author.objects.update(**serializer.validated_data, id=author_id)
            
            return Response(serializer.data)
   
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InboxSerializerObjects:
    def deserialize_inbox_objects(self, item, context={}):
        object_model = item.content_type.model_class()
        if object_model is Post:
            serializer = PostSerializer
        elif object_model is Like:
            serializer = LikeSerializer
        elif object_model is Comment:
            serializer = CommentSerializer
        
        return serializer(item.content_object, context=context).data
    
    def serialize_inbox_objects(self, data, context={}):
        type = data.get('type')
        if type is None:
            raise exceptions
        if type == Post.get_api_type():
            serializer = PostSerializer
        elif type == Like.get_api_type():
            serializer = LikeSerializer
        elif type == Comment.get_api_type():
            serializer = CommentSerializer
        return serializer(data=data, context=context)

class Inbox_list(APIView, InboxSerializerObjects, PageNumberPagination):
    serializer_class = InboxSerializer
    pagination_class = InboxSetPagination

    def get(self, request, pk_a):
        author = get_object_or_404(Author,pk=pk_a)
        inbox_data = author.inbox.all()
        paginated_inbox_data = self.paginate_queryset(inbox_data, request)
        return self.get_paginated_response([self.deserialize_inbox_objects(obj) for obj in paginated_inbox_data])
    
    def post(self, request, pk_a):
        author = Author.objects.get(pk=pk_a)
        serializer = self.serialize_inbox_objects(
            self.request.data, context={'author_id': pk_a})
        if serializer.is_valid():
            print("VALIDATED", serializer.validated_data)
            item = serializer.save()
            if hasattr(item, 'update_fields_with_request'):
                item.update_fields_with_request(request)
            inbox_item = Inbox(content_object=item, author=author)
            inbox_item.save()
            return Response({'req': self.request.data, 'saved': model_to_dict(inbox_item)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



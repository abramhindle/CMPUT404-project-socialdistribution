import profile
import re
from django.shortcuts import render
#from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer
from rest_framework.response import Response

class AuthorsView(APIView):
    def get(self,request,*args, **kwargs):
        
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors,many=True)

        return Response(serializer.data)
    
    def post(self,request,*args, **kwargs):
        author_data = request.data

        new_author = Author.objects.create(display_name=author_data["display_name"],profile_image=author_data["profile_image"],github_handle=author_data["github_handle"])

        new_author.save()
        serializer = AuthorSerializer(new_author)

        return Response(serializer.data)
        

class SingleAuthorView(APIView):
    def get(self,request,author_id,*args, **kwargs):
        author = Author.objects.get(id=author_id)
        serializer = AuthorSerializer(author)

        return Response(serializer.data)
        
        
    
    def post(self,request,author_id,*args, **kwargs):
        author_data = request.data
        
        update_author_id = Author.objects.filter(id=author_id).update(display_name=author_data["display_name"],profile_image=author_data["profile_image"],github_handle=author_data["github_handle"])

        update_author = Author.objects.get(id=update_author_id)
        
        update_author.save()
        serializer = AuthorSerializer(update_author)

        return Response(serializer.data)


# Create your views here.

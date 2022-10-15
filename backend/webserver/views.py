import profile
import re
from django.shortcuts import render
#from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer
from rest_framework.response import Response

class AuthorView(APIView):
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
       
# Create your views here.

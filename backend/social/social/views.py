from django.shortcuts import  render, redirect
from django.contrib.auth import login
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth.models import User
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from author.models import Author
from author.serializers import AuthorSerializer
from rest_framework import status

from django.db import transaction, IntegrityError
from django.contrib.auth.backends import AllowAllUsersModelBackend
from rest_framework_simplejwt.tokens import RefreshToken
from social.serializers import UserSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse

class register(APIView):
    def post(self, request):
        """Register a django user to make them an author"""
        id_ = str(uuid.uuid4())
        display_name = request.data['username']
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.create_user(username=display_name, email=email, password=password)
            user.save()
            url = "authors/" + id_
            author = Author(user=user, id = id_, displayName= display_name, url=url)
            author.save()
            return(Response(id_, status=status.HTTP_201_CREATED))
        except IntegrityError as e: 
            if 'unique constraint' in e.args:
               return(Response("display name already in use", status=status.HTTP_400_BAD_REQUEST)) 


class login(APIView):
    def post(self, request):
        """deals with user auth"""
        username = request.data['username']
        password = request.data['password']
        auth = AllowAllUsersModelBackend()

        user = auth.authenticate(request=request, username=username, password= password)

        author= Author.objects.filter(displayName=username)[0]

        params = {}
        # params['user'] = UserSerializer(user)
        # params['token'] = get_token()
        params = AuthorSerializer(author)

        if not user:
            return Response("user not registered", status=status.HTTP_401_UNAUTHORIZED)
        return Response(params.data, status=status.HTTP_202_ACCEPTED)
    

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})
    
class logout(APIView):
    def post(self, request):
        """deals with user auth"""
        auth = AllowAllUsersModelBackend()
        
        user = auth.logout(request=request)
        return Response( status=status.HTTP_202_ACCEPTED)
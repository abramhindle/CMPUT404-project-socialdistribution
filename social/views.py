from django.shortcuts import  render, redirect
from django.contrib.auth import login, logout
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
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

custom_parameter = openapi.Parameter(
    name='custom_param',
    in_=openapi.IN_QUERY,
    description='A custom parameter for the POST request',
    type=openapi.TYPE_STRING,
    required=True,
)


from rest_framework import viewsets
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
import os

@authentication_classes([])
@permission_classes([])
class register(APIView):
    def post(self, request):
        """Register a django user to make them an author"""
        id_ = str(uuid.uuid4())
        display_name = request.data['username']
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.create_user(username=display_name, email=email, password=password)
            user.is_active = False
            user.save()
            url = "authors/" + id_
            author = Author(user=user, id = id_, displayName= display_name, url=url)
            author.save()
            return(HttpResponse(id_, status=status.HTTP_201_CREATED))
        except IntegrityError as e: 
            if 'unique constraint' in e.args:
               return(HttpResponse("display name already in use", status=status.HTTP_400_BAD_REQUEST))
        

@authentication_classes([])
@permission_classes([])
class login(APIView):
    def post(self, request):
        """deals with user auth"""
        username = request.data['username']
        password = request.data['password']
        auth = AllowAllUsersModelBackend()
    
        user = auth.authenticate(request=request, username=username, password= password)
        if not user:
            return Response("user not registered", status=status.HTTP_401_UNAUTHORIZED)

        if user.is_active == True:
            author= Author.objects.filter(displayName=username)[0]
            params = AuthorSerializer(author)
            return Response(params.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response("user needs to wait for approval from a server admin", status=status.HTTP_402_PAYMENT_REQUIRED)

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})
    
# class logout(APIView):
@authentication_classes([])
@permission_classes([])
def logout_view(request):
    logout(request)
    return Response( status=status.HTTP_202_ACCEPTED)
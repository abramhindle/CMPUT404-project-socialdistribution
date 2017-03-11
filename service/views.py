from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.


# ViewSets define the view behavior.
from rest_framework import viewsets
from service.serializers import UserSerializer, AuthorSerializer
from dashboard.models import Author


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

from django.shortcuts import render

from rest_framework import viewsets

from .serializers import AuthorSerializer, FollowerSerializer
from .models import Author, Follower

# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all().order_by('id')
    serializer_class = FollowerSerializer
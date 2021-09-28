from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import AuthorSerializer

from .models import Author
# Create your views here.

# https://www.django-rest-framework.org/tutorial/3-class-based-views/
class AuthorList(APIView):
    """
    List all authors
    """
    @extend_schema(
        request=AuthorSerializer,
        responses=AuthorSerializer(many=True), # specify response format
    )
    def get(self, request):
        authors = Author.objects.all() 
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class AuthorDetail(APIView):

    """
    retrieve or update author profile
    """
    @extend_schema(
        request=AuthorSerializer,
        responses=AuthorSerializer,
    )
    def get(self, request, author_id):
        author = Author.objects.get(pk=author_id)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)

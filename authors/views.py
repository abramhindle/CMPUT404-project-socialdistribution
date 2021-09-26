from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import AuthorSerializer

from .models import Author
# Create your views here.

# https://www.django-rest-framework.org/tutorial/3-class-based-views/
class AuthorList(APIView):
    """
    List all authors
    """
    def get(self, request):
        authors = Author.objects.all() 
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

@api_view()
def author_root(request):
    return Response([
        "/author/<author_id:uuid>",
    ])


class AuthorDetail(APIView):
    """
    retrieve or update author profile
    """
    def get(self, request, author_id):
        author = Author.objects.get(pk=author_id)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)

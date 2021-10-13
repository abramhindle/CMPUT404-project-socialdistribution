from django.shortcuts import render

from rest_framework import viewsets

from .serializers import AuthorSerializer
from .models import Author

# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
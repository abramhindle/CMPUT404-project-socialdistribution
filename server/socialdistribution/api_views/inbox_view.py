from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import Author, Follow
from socialdistribution.serializers import AuthorSerializer

@api_view(['GET', 'POST', 'DELETE'])
def inbox_detail(request, authorID):
    pass



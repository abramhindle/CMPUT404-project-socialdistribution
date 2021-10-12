from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
import json
# Create your views here.

class index(APIView):
    pass

class comments(APIView):
    pass

class post(APIView):
    pass

class likes(APIView):
    pass

class commentLikes(APIView):
    pass
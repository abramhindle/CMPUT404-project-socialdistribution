from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
import json
from django.core.paginator import Paginator

class index(APIView):
    pass

class comments(APIView):
    def get(self, request):
        page = request.query_params.get("page")
        return Response(status=200)

    def post(self, request, comment):
        pass

class post(APIView):
    pass

class likes(APIView):
    pass

class commentLikes(APIView):
    pass
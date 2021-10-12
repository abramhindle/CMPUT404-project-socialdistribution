from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Author, Inbox, Follow
from .serializers import AuthorSerializer
import json

class index(APIView):
    pass

class profile(APIView):
    pass

class followers(APIView):
    def get(self, request, author_id):
        follower_ids = Follow.objects.filter(toAuthor=author_id)
        print("Q1:")
        print(follower_ids)
        follower_profiles = Author.objects.filter(authorID__in=follower_ids.values_list('fromAuthor', flat=True))
        print("Q2: ")
        print(follower_profiles)
        serializer = AuthorSerializer(follower_profiles, many=True)
        response = {'type': 'followers', 'items': serializer.data}
        print("response: ")
        print(response)
        return Response(response)

class follower(APIView):
    pass

class liked(APIView):
    pass

class inbox(APIView):
    pass
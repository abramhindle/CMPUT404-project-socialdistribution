from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
import json
from django.core.paginator import Paginator
from .serializers import CommentSerializer

class index(APIView):
    pass

class comments(APIView):
    def get(self, request, author_id, post_id):
        try:
            post_comments = Comment.objects.filter(postID=post_id).order_by("date")
        except:
            return Response("The requested post does not exist.", status=404)
        size = request.query_params.get("size", 5)
        page = request.query_params.get("page", 1)
        paginator = Paginator(post_comments, size)
        comment_serializer = CommentSerializer(paginator.get_page(page), many=True)
        url = request.build_absolute_uri('')
        post = url[:-len("/comments")]
        response = {"type": "comments", "page": page, "size": size, "post": post, "id": url, "comments": comment_serializer.data}
        return Response(response, status=200)

    def post(self, request, comment):
        pass

class post(APIView):
    pass

class likes(APIView):
    pass

class commentLikes(APIView):
    pass
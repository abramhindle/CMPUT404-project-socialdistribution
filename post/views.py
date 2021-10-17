from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
from author.models import Author
import json
from django.core.paginator import Paginator
from .serializers import CommentSerializer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class index(APIView):
    pass

class comments(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(postID=post_id, ownerID=author_id)
            post_comments = Comment.objects.filter(postID=post_id).order_by("-date")
        except Exception as e:
            print(e)
            return Response("The requested post does not exist.", status=404)
        if not post.isPublic and str(request.user.author.authorID) != author_id:
            # only the author of the post can view the comments if the post is not public
            return Response("This post's comments are private.", status=403)
        size = request.query_params.get("size", 5)
        page = request.query_params.get("page", 1)
        try:
            paginator = Paginator(post_comments, size)
            comment_serializer = CommentSerializer(paginator.get_page(page), many=True)
        except:
            return Response("Bad request. The size query parameter must be a positive integer.", status=400)
        url = request.build_absolute_uri('')
        post_url = url[:-len("/comments")]
        response = {"type": "comments", "page": page, "size": size, "post": post_url, "id": url, "comments": comment_serializer.data}
        return Response(response, status=200)

    def post(self, request, author_id, post_id):
        print(request.data)
        comment_serializer = CommentSerializer(data=request.data, context={"post_id": post_id, "author_id": author_id})
        if comment_serializer.is_valid():
            comment_serializer.save()
        else:
            return Response("Malformed request.", status=400)
        return Response("Comment created.", status=200)
        

class post(APIView):
    pass

class likes(APIView):
    pass

class commentLikes(APIView):
    pass
from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from author.models import Author
import json
from django.core.paginator import Paginator
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class index(APIView):
    def get(self,request,author_id):
        post_ids = Post.objects.filter(ownerID=author_id)
        if not post_ids:
            return Response(status = 404)
        serializer = PostSerializer(post_ids, many=True)
        response = {'type':'posts', 'items': serializer.data}
        return Response(response)

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
        try:
            size = int(request.query_params.get("size", 5))
            page = int(request.query_params.get("page", 1))
            paginator = Paginator(post_comments, size)
            comment_serializer = CommentSerializer(paginator.get_page(page), many=True)
        except:
            return Response("Bad request. Invalid size or page parameters.", status=400)
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
        

# all owners posts
class post(APIView):

    def get(self,request,author_id, post_id):
        post_ids = Post.objects.filter(ownerID=author_id, postID=post_id)
        if not post_ids:
            return Response(status = 404)

        serializer = PostSerializer(post_ids, many=True)
        response = {'type':'posts', 'items': serializer.data}
        return Response(response)

    def post():
        pass

    def put():
        pass

    def delete():
        pass

class likes(APIView):
    def get(self,request,author_id,post_id):
        likes = Like.objects.filter(authorID=author_id,postID=post_id)
        if not likes:
            return Response(status = 404) #consider replacing with no likes for this post
        serializer = LikeSerializer(likes,many = True)
        response = {'type':'likes','items': serializer.data}
        return Response(response)
class commentLikes(APIView):
    pass

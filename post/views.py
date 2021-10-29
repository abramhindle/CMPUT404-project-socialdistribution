from django.shortcuts import render
from django.db.models import Subquery
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from author.models import Author, Follow, Inbox
import json
from django.core.paginator import InvalidPage, Paginator
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import uuid
from datetime import datetime, timezone
from django.contrib.contenttypes.models import ContentType

class index(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self,request,author_id):
        # Get all the public and listed posts for this author
        post_ids = Post.objects.filter(ownerID=author_id, isPublic=True, isListed=True).order_by("-date")
        # Get all the posts for this author if the author is making the request instead
        if request.user.is_authenticated and request.user.author and str(request.user.author.authorID) == author_id:
            post_ids = Post.objects.filter(ownerID=author_id)


        if not post_ids:
            return Response(status = 404)
        try:
            size = int(request.query_params.get("size",5)) #5 is default right?
            page = int(request.query_params.get("page",1)) #By default, 1 object per page.
            paginator = Paginator(post_ids, size)
        except:
            return Response("Bad request. Invalid size or page parameters.", status=400)
        try :
            serializer = PostSerializer(paginator.page(page), many=True)
            pageData = serializer.data
        except InvalidPage:
            pageData = []
        response = {'type':'posts','page':page, 'size':size, 'items': pageData}
        return Response(response)

    #create a post and generate id
    def post(self,request,author_id):
        if request.user.is_authenticated and request.user.author and str(request.user.author.authorID) == author_id:
            serializer = PostSerializer(data=request.data, context={"ownerID": author_id})
            if serializer.is_valid():
                post = serializer.save()
                # If the post is listed send it to all of the author's followers
                if post.isListed:
                    follows = Follow.objects.filter(toAuthor=author_id)
                    for follow in follows:
                        Inbox.objects.create(authorID=follow.fromAuthor, inboxType="post", fromAuthor=request.user.author, date=post.date, objectID=post.postID, content_type=ContentType.objects.get(model="post"))
                return Response(serializer.data, status=201)
            else:
                print(serializer.errors)
                return Response(status=400)
        else:
            # Make sure authors can't create posts under someone elses account
            return Response(status=403)




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

    def post(self,request,author_id,post_id):
        comment_serializer = CommentSerializer(data=request.data, context={"post_id": post_id, "author_id": author_id})
        if comment_serializer.is_valid():
            comment_serializer.save()
        else:
            return Response("Malformed request.", status=400)
        return Response("Post created.", status=200)

# all owners posts
class post(APIView):
    #authentication stuff
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self,request,author_id, post_id):
        try:
            post = Post.objects.get(ownerID=author_id, postID=post_id)
        except Post.DoesNotExist:
            return Response(status = 404)
        # only return public posts unless you own the post or follow the owner of the post
        #author = Author.objects.get(author_id)
        is_author_friend = Follow.objects.filter(toAuthor=author_id, fromAuthor=str(request.user.author.authorID)).exists()
        if not post.isPublic and str(request.user.author.authorID) != author_id and not is_author_friend:
            return Response(status = 403)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    #update the post with postId in url
    def post(self,request,author_id,post_id):
        if request.user.is_authenticated:
            try:
                author = request.user.author
            except:
                # The user does not have an author profile
                return Response(status=403)
            if str(author.authorID) != author_id:
                # The request was made by a different author
                return Response(status=403)
            try:
                post = Post.objects.get(ownerID=author_id,postID=post_id)
                update_data = request.data
                #print(update_data)
                serializer = PostSerializer(post,data=update_data, partial=True)
                #print(serializer.is_valid())
                if serializer.is_valid():
                    serializer.save()
                    # print(serializer.data)
                    # returns the updated post
                    return JsonResponse(serializer.data, status=201)
                    print(serializer.errors)
                return Response(status=422)
            except Post.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=401)


    #create a post with that id in the url
    def put(self,request,author_id,post_id):
        if str(request.user.author.authorID) != author_id:
            # Make sure authors can't create posts under someone elses account
            return Response(status=403)
        if Post.objects.filter(ownerID=author_id, postID = post_id).exists():
            return Response(status=409)
        post = Post.objects.create(ownerID=request.user.author, postID=post_id, date=datetime.now(timezone.utc).astimezone(), isPublic=True, isListed=True, hasImage=False)
        post.save()
        return Response(status=201)

    def delete(self,request,author_id,post_id):
        if str(request.user.author.authorID) != author_id:
            # Only the owner of the Post can delete it
            return Response(status=403)
        try:
            Post.objects.get(ownerID=author_id,postID=post_id).delete()
        except:
            return Response("No such post exists, Delete unsuccessful.",status=404)
        return Response(status=200)

class likes(APIView):
    def get(self,request,author_id,post_id):
        if not Post.objects.filter(postID=post_id, ownerID=author_id).exists():
            return Response(status=404)
        likes = Like.objects.filter(objectID=post_id)
        serializer = LikeSerializer(likes,many = True)
        response = {'type':'likes','items': serializer.data}
        return Response(response)

class commentLikes(APIView):
    def get(self,request,author_id,post_id,comment_id):
        if not Post.objects.filter(postID=post_id, ownerID=author_id).exists() or not Comment.objects.filter(commentID=comment_id, postID=post_id).exists():
            return Response(status=404)
        likes = Like.objects.filter(authorID=author_id, objectID=comment_id)
        #print(likes)
        serializer = LikeSerializer(likes,many = True)
        response = {'type':'likes','items': serializer.data}
        return Response(response)

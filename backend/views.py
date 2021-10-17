from functools import partial
from django.db.models.query_utils import refs_expression
from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AuthorSerializer, CommentSerializer, PostSerializer
from .models import Author, Post

# Create your views here.

# Helper function on getting an author based on author_id
def _get_author(author_id):
    try:
        author = Author.objects.get(id=author_id)
    except:
        return None
    return author

# Helper function on getting the follower from an author using the follower_id
def _get_follower(author, follower_id):
    try:
        follower = author.followers.get(id=follower_id)
    except:
        return None
    return follower

@api_view(['GET'])
def authors_list_api(request):
    """
    This will return the list of authors currently on the server.

    args:
        request - A request to get a list of authors
    return:
        A Response (status=200) with type:"authors" and items that contains the list of author. 
    """
    authors = list(Author.objects.all())

    author_serializer = AuthorSerializer(authors, many=True)
    authors_dict = {
        "type": "authors",
        "items": author_serializer.data
    }
    return Response(authors_dict)

# https://www.django-rest-framework.org/tutorial/3-class-based-views/
class AuthorDetail(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
        except:
            return HttpResponseNotFound("Author Not Found")
        
        author_serializer = AuthorSerializer(author)
        author_dict = author_serializer.data
        author_dict["type"] = "author"
        return Response(author_dict)
    
    def post(self, request, author_id):
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
        
        author_serializer = AuthorSerializer(author, data=request.data, partial=True)
        if author_serializer.is_valid():
            author = author_serializer.save()
            author.update_url_fields_with_request(request)
            return Response(author_serializer.data)
        
        return Response(author_serializer.error, status=400)


class FollowerDetail(APIView):
    
    def get(self, request, author_id, foreign_author_id=None):
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        if foreign_author_id is not None:
            follower = self._get_follower(author, foreign_author_id)
            if follower == None:
                return HttpResponseNotFound("Following Author Not Found")
            follower_serializer = AuthorSerializer(follower)
            follower_dict = follower_serializer.data
            follower_dict['type'] = "follower"
            return Response(follower_dict)

        followers = list(author.followers.all())
        follower_serializer = AuthorSerializer(followers, many=True)
        followers_dict = {
            "type": "followers",
            "items": follower_serializer.data
        }
        return Response(followers_dict)

    def put(self, request, author_id, foreign_author_id):
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        follower_serializer = AuthorSerializer(data=request.data)
        if follower_serializer.is_valid():
            print(follower_serializer.validated_data)

        
    def delete(self, request, author_id, foreign_author_id):
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
        follower = _get_follower(author, foreign_author_id)
        if follower == None:
            return HttpResponseNotFound("Following Author Not Found")
        author.followers.remove(follower)
        return Response({"detail":"id {} successfully removed".format(follower.id)},status=200)

@api_view(['GET'])
def post_view_api(request, id, post_id=None):
    try:
        author = Author.objects.get(id=id)
    except:
        return Response(status=404)
    
    if post_id is not None:
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(status=404)
        
        post_serializer = PostSerializer(post)
        post_dict = post_serializer.data
        post_dict['type'] = "post" 
        return Response(post_dict)
    
    posts = list(author.posted.all())
    post_serializer = PostSerializer(posts, many=True)
    posts_dict = {
        "type": "post",
        "items": post_serializer.data
    }
    return Response(posts_dict)

@api_view(['GET'])
def comment_view_api(request, id, post_id):
    try:
        author = Author.objects.get(id=id)
        post = author.posted.get(id=post_id)
    except: 
        return Response(status=404)
    
    comments_dict = {
        "type":"comments",
        "items": []
    }
    comments = post.comments.all()
    for comment in comments:
        comment_author_dict = AuthorSerializer(Author.objects.get(id=comment.author.id)).data
        comment_dict = {
            "type": "comment",
        }
        comment_dict["author"] = comment_author_dict
        comment_dict["author"]["type"] = "author"
        comment_dict.update(CommentSerializer(comment).data)
        comments_dict["items"].append(comment_dict)

    return Response(comments_dict)
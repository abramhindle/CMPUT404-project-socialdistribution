import json
import uuid
import typing
from functools import partial
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import AuthorSerializer, CommentSerializer, PostSerializer
from .models import Author, Post
from .forms import SignUpForm

# Helper function on getting an author based on author_id
def _get_author(author_id: str) -> Author:
    try:
        author = Author.objects.get(id=author_id)
    except:
        return None
    return author

# Helper function on getting the follower from an author using the follower_id
def _get_follower(author: Author, follower_id: str) -> Author:
    try:
        follower = author.followers.get(id=follower_id)
    except:
        return None
    return follower

# Helper function on getting the post from an author object
def _get_post(author: Author, post_id: str) -> Post:
    try:
        post = author.posted.get(id=post_id)
    except:
        return None
    return post
    
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

@login_required
def home(request):
    """
    The home view after a successful login which will redirect to the author's homepage

    args:
        - request : The request after a successful login
    return:
        - HttpResponseRedirect : A redirect to the author's homepage
    """
    user = request.user
    author_id = user.author.id
    return HttpResponseRedirect(reverse("author-detail", args=[author_id]))

@login_required
def admin_approval(request):
    """
    The admin approval view after a successful signup

    args:
        - request : The request after a successful singup
    return:
        - render : Show the waiting for admin approval page
    """
    return render(request, "admin_approval.html")

@api_view(['GET','POST'])
def signup(request):
    """
    This will return the signup view 

    args:
        - request : A request to signup 
    returns:
        - redirect : If the request is a POST
        - render : If the request is a GET 
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # Load the profile from instance created by the signal
            user.author.display_name = form.cleaned_data.get("display_name")
            user.author.github_url = form.cleaned_data.get("github_url")
            user.is_active = False
            user.save()
            user.author.update_url_fields_with_request(request)
            return redirect('admin-approval')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@api_view(['GET'])
def authors_list_api(request: Request):
    """
    This will return the list of authors currently on the server.

    args:
        - request - A request to get a list of authors
    
    return:
        - A Response (status=200) with type:"authors" and items that contains the list of author. 
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

    def get(self, request: Request, author_id: str):
        """
        This will get the author's profile

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
        
        return:
            - If author is found, a Response of the author's profile in JSON format is returned
            - If author is not found, a HttpResponseNotFound is returned
        """
        try:
            author = Author.objects.get(id=author_id)
        except:
            return HttpResponseNotFound("Author Not Found")
        
        author_serializer = AuthorSerializer(author)
        author_dict = author_serializer.data
        return Response(author_dict)
    
    def post(self, request: Request, author_id: str):
        """
        This will update the author's profile

        args:
            _ request - A request to get the author
            _ author_id - The uuid of the author to get 
        
        return:
            - If author is found, a Response of the author's profile in JSON format is returned
            - If author is not found, a HttpResponseNotFound is returned
            - If the serializer had an issues a Response returned with a status=400 argument. 
        """
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
    def get(self, request: Request, author_id: str, foreign_author_id: str = None):
        """
        This will get the author's followers

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - foreign_author_id - The uuid of the follower 

        return:
             
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        if foreign_author_id is not None:
            follower = _get_follower(author, foreign_author_id)
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

    def put(self, request: Request, author_id: str, foreign_author_id: str):
        """
        This will add a follower to the author provided.

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - foreign_author_id - The uuid of the follower 

        return:
             
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        follower = Author.objects.get(id=foreign_author_id)
        # If the follower doesn't exist in our database then we create a new Author
        if follower == None:
            return HttpResponseNotFound("Follower Not Found")
        
        author.followers.add(follower)
        return Response({"detail":"id {} successfully added".format(follower.id)},status=200)

    def delete(self, request: Request, author_id: str, foreign_author_id: str):
        """
        This will delete a follower from the author provided.

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - foreign_author_id - The uuid of the follower 

        return:
             
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
        follower = _get_follower(author, foreign_author_id)
        if follower == None:
            return HttpResponseNotFound("Following Author Not Found")
        author.followers.remove(follower)
        return Response({"detail":"id {} successfully removed".format(follower.id)},status=200)

class PostDetail(APIView):
    def get(self, request: Request, author_id: str, post_id: str = None):
        """
        This will get a Author's post or list of posts

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
             
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        if post_id is not None:
            post = _get_post(author, post_id)
            if post == None:
                return HttpResponseNotFound("Post Not Found")
            
            post_serializer = PostSerializer(post)
            return Response(post_serializer.data)
                
        posts = list(author.posted.all())
        post_serializer = PostSerializer(posts, many=True)
        post_dict = {
            "items": post_serializer.data
        }
        return Response(post_dict)

    
    def post(self, request: Request, author_id: str, post_id: str = None):
        """
        This will update or create a new post

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
             
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        request_dict = dict(request.data)

        if post_id is not None:
            post = _get_post(author, post_id)
            if post == None:
                return HttpResponseNotFound("Post Not Found")
            post_serializer = PostSerializer(post, data=request_dict, partial=True)
            if post_serializer.is_valid():
                post = post_serializer.save()
                return Response(post_serializer.data)
        
        uuid_id = uuid.uuid4()
        url =  request.build_absolute_uri(reverse("author-posts",args=[author_id])) + '/' + str(uuid_id)
        request_dict['id'] = str(uuid_id)
        request_dict['url'] = url
        print(request_dict)
        post_serializer = PostSerializer(data=request_dict)

        if post_serializer.is_valid():
            post = post_serializer.save()
            post.url = url
            return Response(post_serializer.data)
        
        return HttpResponseBadRequest("Malformed request - error(s): {}".format(post_serializer.errors))

    def delete(self, request: Request, author_id: str, post_id: str):
        """
        This delete get a Author's post

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
             
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
        
        post = _get_post(author, post_id)
        if post == None:
            return HttpResponseNotFound("Post Not Found")
        post_id = post.id
        post.delete()
        return Response({"detail":"post id {} successfully removed".format(post_id)},status=200)

    def put(self, request: Request, author_id: str, post_id: str):
        """
        This will get a Author's post(s)

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
             
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        request_dict = request.data
        pass


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



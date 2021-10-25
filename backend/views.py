import json
import uuid
import typing
from functools import partial
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import AuthorSerializer, CommentSerializer, PostSerializer, PostsLikeSerializer, CommentsLikeSerializer
from .models import Author, Post,Comment
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

# Helper function on getting the comment from a post object
def _get_comment(post: Post, comment_id) -> Comment:
    try:
        comment = post.comments.get(id=comment_id)
    except:
        return None
    return comment
    
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

@login_required
def home(request: Request) -> HttpResponseRedirect:
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
def admin_approval(request: Request) -> HttpResponse:
    """
    The admin approval view after a successful signup

    args:
        - request : The request after a successful singup
    return:
        - render : Show the waiting for admin approval page
    """
    return render(request, "admin_approval.html")

@api_view(['GET','POST'])
def signup(request: Request):
    """
    This will return the signup view 

    args:
        - request : A request to signup 

    returns:
        - redirect : If the request is a POST
        - render : If the request is a GET 
    """
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # Load the profile from instance created by the signal
            user.author.display_name = form.cleaned_data.get("display_name")
            user.author.github_url = form.cleaned_data.get("github_url")
            user.author.profile_image = form.cleaned_data.get("profile_image")
            user.is_active = False
            user.save()
            user.author.update_url_fields_with_request(request)
            return HttpResponse("Signup Successful: Please wait for admin approval.")
        else:
            return HttpResponseBadRequest()
    else:
        return render(request, 'signup.html', {'form': form})

@api_view(['GET'])
def authors_list_api(request: Request):
    """
    This will return the list of authors currently on the server.

    args:
        - request : A request to get a list of authors
    
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
    """
    This class implements all the Author specific views
    """
    def get(self, request: Request, author_id: str):
        """
        This will get the author's profile

        args:
            - request : A request to get the author
            - author_id : The uuid of the author to get 
        
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
            _ request : A request to get the author
            _ author_id : The uuid of the author to get 
        
        return:
            - If author is found, a Response of the author's updated profile in JSON format is returned
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
    """
    This class implements all the Follower specific views
    """
    def get(self, request: Request, author_id: str, foreign_author_id: str = None):
        """
        This will get the author's followers

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - foreign_author_id - The uuid of the follower 

        return:
            - If a follower is found, a Response of the follower's profile in JSON format is returned
            - If author (or follower if specified) is not found, a HttpResponseNotFound is returned
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
            - If a follower is found, a Response of the follower's id is returned
            - If author or follower is not found, a HttpResponseNotFound is returned 
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
            - If a follower is found, a Response of the follower's id is returned
            - If author or follower is not found, a HttpResponseNotFound is returned 
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
    """
    This class implements all the Post specific views
    """
    def get(self, request: Request, author_id: str, post_id: str = None):
        """
        This will get a Author's post or list of posts

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
            - If a post is found, a Response of the post's detail in JSON format is returned
            - If author (or post if specified) is not found, a HttpResponseNotFound is returned 
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
            - A Response of the new or updated post in JSON format is returned
            - If author is not found, a HttpResponseNotFound is returned
            - If the serializer had an issues a Response returned with a status=400 argument. 
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
            - If a post is found, a Response of the post's id is returned
            - If author or post is not found, a HttpResponseNotFound is returned 
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
            - A Response of the new post in JSON format is returned
            - If author is not found, a HttpResponseNotFound is returned
            - If the serializer had an issues a Response returned with a status=400 argument.
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")

        request_dict = dict(request.data)
        url =  request.build_absolute_uri(reverse("author-posts",args=[author_id])) + '/' + str(post_id)
        request_dict['url'] = url
        request_dict['id'] = post_id
        post_serializer = PostSerializer(data=request_dict)

        if post_serializer.is_valid():
            post = post_serializer.save()
            post.url = url
            return Response(post_serializer.data)
        
        return HttpResponseBadRequest("Malformed request - error(s): {}".format(post_serializer.errors))

class CommentDetail(APIView):
    def get(self, request: Request, author_id: str, post_id: str):
        """
        This will get the list of comments

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
            - If a post is found, a Response of the list of comments in JSON format is returned
            - If author (or post if specified) is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
        
        post = _get_post(author, post_id)
        if post == None:
            return HttpResponseNotFound("Post Not Found")
        
                
        comments = list(post.comments.all())
        comment_serializer = CommentSerializer(comments, many=True)
        comment_dict = {
            "type":"comments", 
            "items": comment_serializer.data
        }
        return Response(comment_dict)

    # def post(self, request: Request, author_id: str, post_id: str):
    #     author = _get_author(author_id)
    #     if author == None:
    #         return HttpResponseNotFound("Author Not Found")
        
    #     request_dict = dict(request.data)
    #     comment_id = request_dict['id']
    #     comment_uuid = comment_id[comment_id.rfind('/')+1:]
    #     request_dict['id'] = comment_uuid
    #     url =  request.build_absolute_uri(reverse("comment-detail",args=[author_id, post_id])) + '/' + str(comment_uuid)
    #     request_dict['url'] = url
    #     comment_post = Post.objects.get(id=post_id)
    #     request_dict['post'] = post_id
    #     # print(request_dict)
    #     comment_serializer = CommentSerializer(data=request_dict)

    #     if comment_serializer.is_valid():
    #         comment = comment_serializer.save()

    #         return Response(comment_serializer.data)

    #     return HttpResponseBadRequest("Malformed request - error(s): {}".format(comment_serializer.errors))
class LikedDetail(APIView):
    """
    This class implements all the Liked specific views
    """
    def get(self, request: Request, author_id: str):
        """
        This will get what an author has liked

        args:
            - request - A request to get the author's liked
            - author_id - The uuid of the author to get 

        return:
            - A Response of the author's liked comments or posts in JSON format is returned
            - If author is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
                
        comments_liked = list(author.comments_liked.all())
        posts_liked = list(author.posts_liked.all())
        posts_liked_serializer = PostsLikeSerializer(posts_liked, many=True)
        comments_liked_serializer = CommentsLikeSerializer(comments_liked, many=True)
        liked_serializer_data = posts_liked_serializer.data + comments_liked_serializer.data
        liked_dict = {
            "type":"liked",
            "items": liked_serializer_data
        }
        return Response(liked_dict)

class PostLikesDetail(APIView):
    """
    This class implements all the Post Likes specific views
    """
    def get(self, request: Request, author_id: str, post_id: str):
        """
        This will get the likes a post has

        args:
            - request - A request to get the post's likes
            - author_id - The uuid of the author who created the post
            - post_id - The uuid of the post we want the like of

        return:
            - A Response of the posts's likes in JSON format is returned
            - If author or post is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
        
        post = _get_post(author, post_id)
        if post == None:
            return HttpResponseNotFound("Post Not Found")
                
        post_likes = list(post.likes.all())
        post_likes_serializer = PostsLikeSerializer(post_likes, many=True)
        likes_dict = {
            "type":"likes",
            "items": post_likes_serializer.data
        }
        return Response(likes_dict)

class CommentLikesDetail(APIView):
    """
    This class implements all the Comment Likes specific views
    """
    def get(self, request: Request, author_id: str, post_id: str, comment_id: str):
        """
        This will get the likes a comment has

        args:
            - request - A request to get the comments likes
            - author_id - The uuid of the author to get 

        return:
            - A Response of the author's liked comments or posts in JSON format is returned
            - If author is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            return HttpResponseNotFound("Author Not Found")
        
        post = _get_post(author, post_id)
        if post == None:
            return HttpResponseNotFound("Post Not Found")

        comment = _get_comment(post,comment_id)
        if comment == None:
            return HttpResponseNotFound("Comment Not Found")
                
        comment_likes = list(comment.likes.all())
        comment_likes_serializer = CommentsLikeSerializer(comment_likes, many=True)
        likes_dict = {
            "type":"likes",
            "items": comment_likes_serializer.data
        }
        return Response(likes_dict)
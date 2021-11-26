import json
import uuid
import typing
import requests

from functools import partial
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from .serializers import AuthorSerializer, CommentSerializer, FriendRequestSerializer, PostSerializer, LikeSerializer
from .models import Author, FriendRequest, Post, Comment, Like, Inbox
from .forms import SignUpForm
from .permission import IsAuthenticated, IsAuthorOrReadOnly, IsLocalAuthor
from .converter import *
from .node_connections import send_post_to_foreign_authors, update_db

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

# Helper function on getting the friend from an author using the friend_id
def _get_friend(author: Author, friend_id: str) -> Author:
    try:
        author.followers.get(id=friend_id)
        friend = _get_author(friend_id)
        friend.followers.get(id=author.id)
    except:
        return None
    return friend

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

# Helper function on getting the friend request from an author using the friend_id
def _get_friend_request(sender: Author, recipient: Author) -> FriendRequest:
    try:
        friend_request = FriendRequest.objects.get(object = recipient, actor = sender)
        return friend_request
    except:
        return None
    
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
        - request : The request after a successful signup
    return:
        - render : Show the waiting for admin approval page
    """
    return render(request, "admin_approval.html")

@api_view(['GET','POST'])
@csrf_exempt
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
            user.author.update_url_field()
            Inbox.objects.create(id=user.author)
            return HttpResponse("Signup Successful: Please wait for admin approval.")
        else:
            return HttpResponseBadRequest(form.error_messages)
    else:
        return render(request, 'signup.html', {'form': form})

class LogoutView(APIView):
    def get(self, request: Request):
        """
        This will handle the logout view 

        args: 
            - request : A request to logout

        return:
            - A Response(status=200) to successfully show that the user logged out
        """
        request.session.flush()
        request.user.auth_token.delete()
        return Response(status=200)

@swagger_auto_schema(methods=['get'], responses={200: AuthorSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authors_list_api(request: Request):
    """
    This will return the list of authors (alphabetically sorted by display_name, and paginated) currently on the server.

    args:
        - request : A request to get a list of authors
    
    return:
        - A Response (status=200) with type:"authors" and items that contains the list of author. 
    """
    if IsLocalAuthor(request):
        update_db(True, False)

    author_list = list(Author.objects.all().order_by('display_name'))

    page = request.GET.get('page', 1)
    size = request.GET.get('size', 5)

    paginator = Paginator(author_list, size)

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except InvalidPage:
        authors = paginator.page(1)

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
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: AuthorSerializer, 404: 'Author Not Found'})
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
        if IsLocalAuthor(request):
            update_db(True, False)

        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        author_serializer = AuthorSerializer(author, data=request.data, partial=True)
        if author_serializer.is_valid():

            # Update and save the new author profile of the data is valid
            author = author_serializer.save()
            author.update_url_field()
            return Response(author_serializer.data)

        # Return the cause of the error
        return Response(author_serializer.error, status=400)


class FollowerDetail(APIView):
    """
    This class implements all the Follower specific views
    """
    permission_classes = [IsAuthenticated]
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
        if IsLocalAuthor(request):
            update_db(True, False)

        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        # Check if the foreign author if following the author
        if foreign_author_id is not None:
            follower = _get_follower(author, foreign_author_id)
            if follower == None:
                resp_dict = {'detail':'Follower Author Not Found'}
                return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
            follower_serializer = AuthorSerializer(follower)
            follower_dict = follower_serializer.data
            follower_dict['type'] = "follower"
            return Response(follower_dict)

        # Get the list of the author's followers
        followers = list(author.followers.all().order_by('display_name'))
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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        follower = _get_author(foreign_author_id)
        if follower == None:
            resp_dict = {'detail':'Follower Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        author.followers.add(follower)

        existing_friend_request = _get_friend_request(follower,author)
        if (existing_friend_request != None):
            existing_friend_request.delete()

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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        follower = _get_follower(author, foreign_author_id)
        if follower == None:
            resp_dict = {'detail':'Following Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        author.followers.remove(follower)
        return Response({"detail":"id {} successfully removed".format(follower.id)},status=200)

class FriendDetail(APIView):
    """
    This class implements all the Friend specific views
    """
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, author_id: str, foreign_author_id: str = None):
        """
        This will get the author's friends (ie Author follows and they follow back)

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - foreign_author_id - The uuid of the friend 

        return:
            - If no foreign_author_id a list of friend id and usernames
            - If a friend is found, a Response of the follower's id and username in JSON format is returned
            - If author (or follower if specified) is not found, a HttpResponseNotFound is returned
        """
        author = _get_author(author_id)

        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        if foreign_author_id is not None:
            friend = _get_friend(author, foreign_author_id)
            if friend == None:
                resp_dict = {'detail':'Friend Author Not Found'}
                return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
            friend_serializer = AuthorSerializer(friend)
            friend_dict = friend_serializer.data
            friend_dict['type'] = "friend"
            return Response(friend_dict)
        
        # Get the list of the author's friends
        friends = list(author.followers.all())
        for friend in friends:
            if _get_friend(author, friend.id)==None:
                friends.remove(friend)
        friend_serializer = AuthorSerializer(friends, many=True)
        friends_dict = {
            "type": "friends",
            "items": friend_serializer.data
        }
        return Response(friends_dict)

class PostDetail(APIView):
    """
    This class implements all the Post specific views
    """
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, author_id: str = None, post_id: str = None):
        """
        This will get a Author's post or list of posts

        For the list of posts the results will be sorted by the most recent date and paginated.

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
            - If a post is found, a Response of the post's detail in JSON format is returned
            - If author (or post if specified) is not found, a HttpResponseNotFound is returned 
        """
        if IsLocalAuthor(request):
            update_db(True, True)

        if author_id == None:
            posts_list = list(Post.objects.all().order_by('-published'))
            post_serializer = PostSerializer(posts_list, many=True)
            post_dict = {
                "items": post_serializer.data
            }
            return Response(post_dict)

        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        # If post_id is specified then return that post
        if post_id is not None:
            post = _get_post(author, post_id)
            if post == None:
                resp_dict = {'detail':'Post Not Found'}
                return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
            
            post_serializer = PostSerializer(post)
            post_dict = post_serializer.data
            return Response(post_dict)

        # For getting the list of posts made by the author
        posts_list = list(author.posted.filter(visibility='PUBLIC').order_by('-published'))

        page = request.GET.get('page', 1)
        size = request.GET.get('size', 5)

        paginator = Paginator(posts_list, size)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except InvalidPage:
            posts = paginator.page(1)

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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        request_dict = dict(request.data)
        # Update a post
        if post_id is not None:
            post = _get_post(author, post_id)
            if post == None:
                resp_dict = {'detail':'Post Not Found'}
                return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
                
            post_serializer = PostSerializer(post, data=request_dict, partial=True)
            if post_serializer.is_valid():
                post = post_serializer.save()
                if 'categories' in request_dict:
                    post.categories = json.dumps(request_dict['categories'])
                    post.save()
                return Response(post_serializer.data)
        
        # Create a new post
        request_dict['author'] = AuthorSerializer(author).data
        post_serializer = PostSerializer(data=request_dict)

        if post_serializer.is_valid():
            post = post_serializer.save()
            post.update_url_field()
            if 'categories' in request_dict:
                post.categories = json.dumps(request_dict['categories'])
                post.save()
            send_post_to_foreign_authors(post)
            return Response(post_serializer.data, status=201)
        
        # Return the serializer's error if it failed to create the post
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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        post = _get_post(author, post_id)
        if post == None:
            resp_dict = {'detail':'Post Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        request_dict = dict(request.data)
        request_dict['id'] = post_id
        request_dict['author'] = author
        request_dict.pop('type', None)
        if 'categories' in request_dict:
            request_dict['categories'] = json.dumps(request_dict['categories'])
        # If the id for the post already exist in the db then we update it. 
        # This should be rare though
        post, created = Post.objects.update_or_create(id=post_id, defaults=request_dict)
        post.update_url_field()
        send_post_to_foreign_authors(post)
        post_serializer = PostSerializer(post)


        return Response(post_serializer.data, status=201)
        

class CommentDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, author_id: str, post_id: str):
        """
        This will get the list of comments

        The comments will be sorted by the most recently published date and paginated

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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        post = _get_post(author, post_id)
        if post == None:
            resp_dict = {'detail':'Post Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
                
        comments_list = list(post.comments.all().order_by('-published'))

        page = request.GET.get('page', 1)
        size = request.GET.get('size', 5)

        paginator = Paginator(comments_list, size)

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except InvalidPage:
            comments = paginator.page(1)

        comment_serializer = CommentSerializer(comments, many=True)
        comment_dict = {
            "type": "comments",
            "page": page,
            "size": len(comment_serializer.data),
            "post": str(post.url),
            "comments": comment_serializer.data
        }
        return Response(comment_dict)

    def post(self, request: Request, author_id: str, post_id: str):
        """
        This will get add a comment to the author's post

        args:
            - request - A request to get the author
            - author_id - The uuid of the author to get 
            - post_id - The uuid of the post 

        return:
            - If a post is found, a Response of the comment typed JSON object
            - If author (or post if specified) is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        post = _get_post(author, post_id)
        if post == None:
            resp_dict = {'detail':'Post Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        request_dict = dict(request.data)
        request_dict['post'] = post

        comment_dict = sanitize_comment_dict(request_dict, post)
        # If the id for the comment already exist in the db then we update it. 
        # This should be rare though
        if comment_dict == None:
            bad_request_dict = {"detail":"comment request dict was of bad form"}
            return HttpResponseBadRequest(json.dumps(bad_request_dict), content_type='application/json')
        comment, created = Comment.objects.update_or_create(**comment_dict)
        comment.update_url_field()

        comment_serializer = CommentSerializer(comment)

        return Response(comment_serializer.data, status=201)

class LikedDetail(APIView):
    """
    This class implements all the Liked specific views
    """
    permission_classes = [IsAuthenticated]
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
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        liked = list(author.liked.all())
        liked_serializer = LikeSerializer(liked, many=True)
        liked_dict = {
            "type":"liked",
            "items": liked_serializer.data
        }
        return Response(liked_dict)


class LikesDetail(APIView):
    """
    This class implements all the Likes specific views
    """
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, author_id: str, post_id: str, comment_id: str = None):
        """
        This will get the likes a comment or post has

        args:
            - request - A request to get the likes
            - author_id - The uuid of the author to get 

        return:
            - A Response of the likes on this comments or posts in JSON format is returned
            - If author,post or comment is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        post = _get_post(author, post_id)
        if post == None:
            resp_dict = {'detail':'Post Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        if comment_id != None:
            comment = _get_comment(post,comment_id)
            if comment == None:
                resp_dict = {'detail':'Comment Not Found'}
                return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
            comment_likes = list(Like.objects.filter(object=comment.url))
            comment_likes = LikeSerializer(comment_likes, many=True)
            likes_dict = {
                "type":"likes",
                "items": comment_likes.data
            }
            return Response(likes_dict)
        else:
            post = _get_post(author, post_id)
            if post == None:
                resp_dict = {'detail':'Post Not Found'}
                return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
            post_likes = list(Like.objects.filter(object=post.url)) 
            post_likes = LikeSerializer(post_likes, many=True)
            likes_dict = {
                "type":"likes",
                "items": post_likes.data
            }
            return Response(likes_dict)


    def post(self, request: Request, author_id: str):
        """
        This will post a like for either a comment or a post

        args:
            - request - A request to post a like
            - author_id - The uuid of the author who created the post

        return:
            - A Response detailing the like added
            - If author or the author liking is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        request_dict = dict(request.data)
        # If the author is not a dict but a id/url then we have to convert it to a list
        if not isinstance(request_dict['author'], dict):
            # Check if the like author exist
            try:
                like_author = Author.objects.get(url=request_dict['author'])
            except:
                resp_dict = {'detail':'Like Author Not Found'}
                return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
            request_dict['author'] = AuthorSerializer(data=like_author).data

        like_serializer = LikeSerializer(data=request_dict)
        if like_serializer.is_valid():
            return Response(like_serializer.data, status=200)
        
        return HttpResponseBadRequest("Malformed request - error(s): {}".format(like_serializer.errors))

class InboxDetail(APIView):
    """
    This class will implement all the inbox specific methods
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, author_id: str):
        """
        This will get the inbox of the author

        args:
            - author_id - The uuid of the author

        return:
            - A Response detailing the content of the author's inbox
            - If author or the author's inbox is not found, a HttpResponseNotFound is returned 

        """
        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        try:
            inbox = Inbox.objects.get(id=author)
        except:
            resp_dict = {'detail':"Author's Inbox Not Found"}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        posts_list = list(inbox.posts.all().order_by("-published"))
        likes_list = list(inbox.likes.all())
        friend_requests_list = list(inbox.friend_requests.all())

        post_serializer = PostSerializer(posts_list, many=True)
        like_serializer = LikeSerializer(likes_list, many=True)
        friend_requests_serializer = FriendRequestSerializer(friend_requests_list, many=True)
        res_dict = {
            "type": "inbox",
            "author": str(author.url),
            "items" : []
        }
        res_dict['items'].extend(post_serializer.data)
        res_dict['items'].extend(like_serializer.data)
        res_dict['items'].extend(friend_requests_serializer.data)

        return Response(res_dict, status=200)

        
    def post(self, request: Request, author_id: str):
        """
        This will send a post, like or follow to the author's inbox

        args:
            - request - The request that contains the object to send to the author's inbox
            - author_id - The uuid of the author

        return:
            - A Response detailing the object was successfully sent
            - If author or the author's inbox is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        try:
            inbox = Inbox.objects.get(id=author)
        except:
            resp_dict = {'detail':"Author's Inbox Not Found"}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')

        request_dict = dict(request.data)
        
        if request_dict['type'].lower() == 'post':
            post_dict = sanitize_post_dict(request_dict)
            post, post_created = Post.objects.get_or_create(id=post_dict['id'], defaults=post_dict)
            inbox.posts.add(post)
            if post_created:
                return Response(data={'detail':"Successfully created post object {} and send to recipient's inbox".format(post_dict['url'])}, status=200)
            return Response(data={'detail':"Successfully send post object {} to recipient's inbox".format(post_dict['url'])}, status=200)
            
        
        
        elif request_dict['type'].lower() == 'follow':
            friend_request_dict = sanitize_friend_request_dict(request_dict)

            friend_request, friend_request_created = FriendRequest.objects.get_or_create(
                actor=friend_request_dict['actor'], 
                object=friend_request_dict['object'], 
                defaults=friend_request_dict
            )

            if friend_request_created:
                inbox.friend_requests.add(friend_request)
                friend_request.actor.followers.add(author)
                existing_friend_request = _get_friend_request(author,friend_request.actor)
                if (existing_friend_request != None):
                    existing_friend_request.delete()
                return Response(data={'detail':"Successfully created Friend Request from {} to {} and send to recipient's inbox".format(friend_request.actor.id, author_id)}, status=200)            
            
            return Response(data={'detail':"Friend Request from {} to {} already been sent".format(friend_request.actor.id, author_id)}, status=200)   

        elif request_dict['type'].lower() == 'like':
            like_dict = sanitize_like_dict(request_dict)
            try:
                like, created = Like.objects.get_or_create(
                    author=like_dict['author'], 
                    object=like_dict['object'], 
                    defaults=like_dict
                )
                # If a like object is already created then add it to the inbox
                if created:
                    inbox.likes.add(like)
                    return Response(data={'detail':"Successfully liked object {} and send to recipient's inbox".format(request_dict['object'])}, status=200)
                # If the like object already exist then it was already sent to the inbox
                return Response(data={'detail':"Object {} already liked".format(request_dict['object'])}, status=200)
            except Exception as e:
                return Response(data={'detail':"Object {} already liked".format(request_dict['object'])}, status=200)
        return HttpResponseBadRequest("type: {} not supported".format(request_dict['type']))


    def delete(self, request: Request, author_id: str):
        """
        This will clear the inbox and disassociate all relations of Posts, Likes, and FriendRequests

        args:
            - author_id - The uuid of the author

        return:
            - A Response detailing that the inbox was cleared
            - If author or the author's inbox is not found, a HttpResponseNotFound is returned 
        """
        author = _get_author(author_id)
        if author == None:
            resp_dict = {'detail':'Author Not Found'}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        try:
            inbox = Inbox.objects.get(id=author)
        except:
            resp_dict = {'detail':"Author's Inbox Not Found"}
            return HttpResponseNotFound(json.dumps(resp_dict), content_type='application/json')
        
        inbox.posts.clear()
        inbox.likes.clear()
        inbox.friend_requests.clear()

        return Response({"detail": "Inbox deleted"}, status=200)
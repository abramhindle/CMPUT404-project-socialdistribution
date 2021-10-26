from django.http.response import *
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json
import logging

from cmput404.constants import HOST, API_PREFIX
from socialDistribution.models import *
from .decorators import authenticate_request

# References for entire file:
# Django Software Foundation, "Introduction to class-based views", 2021-10-13
# https://docs.djangoproject.com/en/3.2/topics/class-based-views/intro/
# Django Software Foundation, "JsonResponse objects", 2021-10-13
# https://docs.djangoproject.com/en/3.2/ref/request-response/#jsonresponse-objects

# Need to disable CSRF to make POST, PUT, etc requests. Otherwise, your request needs to contain 'X--CSRFToken: blahblah' with a CSRF token.
# If we need CSRF validation in the future, just remove the csrf_exempt decorators.
#
# Martijn ten Hoor, https://stackoverflow.com/users/6945548/martijn-ten-hoor, "How to disable Django's CSRF validation?",
# 2016-10-12, https://stackoverflow.com/a/39993384, CC BY-SA 3.0
#
# Note: @ensure_crsf_cookie will send the token in the response
# Ryan Pergent, https://stackoverflow.com/users/3904557/ryan-pergent, "how do I use ensure_csrf_cookie?",
# 2017-05-30, https://stackoverflow.com/a/43712324, CC BY-SA 3.0

# Django Software Foundation, "Logging", https://docs.djangoproject.com/en/3.2/topics/logging/
logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Welcome to the Social Distribution API")


@method_decorator(csrf_exempt, name='dispatch')
class AuthorsView(View):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        """ GET - Retrieve all user profiles """

        page = request.GET.get("page")
        size = request.GET.get("size")

        authors = [author.as_json() for author in Author.objects.all()]

        response = {
            "type": "authors",
            "items": authors
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorView(View):

    def get(self, request, author_id):
        """ GET - Retrieve profile of {author_id} """

        author = get_object_or_404(Author, pk=author_id)
        response = author.as_json()
        return JsonResponse(response)

    def post(self, request, author_id):
        """ POST - Update profile of {author_id} """
        return HttpResponse("authors post\nupdate profile")


@method_decorator(csrf_exempt, name='dispatch')
class FollowersView(View):

    def get(self, request, author_id):
        """ GET - Get a list of authors who are the followers of {author_id} """

        author = get_object_or_404(Author, pk=author_id)
        followers = [follower.as_json() for follower in author.followers.all()]

        response = {
            "type": "followers",
            "items": followers
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class LikedView(View):

    def get(self, request, author_id):
        """ GET - Get a list of like objects from {author_id} """
        try:
            author = Author.objects.get(id=author_id)
            authorLikedPosts = Post.objects.filter(likes__exact=author)
            host = request.get_host()
            likes = []
            for post in authorLikedPosts:
                like = {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "summary": f"{author.displayName} Likes your post",
                    "type": "like",
                    "author": author.as_json(),
                    "object": f"http://{host}/author/{post.author.id}/posts/{post.id}"
                }
                likes.append(like)

            response = {
                "type:": "liked",
                "items": likes}

        except Exception as e:
            logger.error(e, exc_info=True)
            return HttpResponseServerError()

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):

    def get(self, request, author_id, post_id):
        return HttpResponse("This is the authors/aid/posts/pid/ endpoint")


@method_decorator(csrf_exempt, name='dispatch')
class PostLikesView(View):

    def get(self, request, author_id, post_id):
        """ GET - Get a list of authors who like {post_id} """
        try:
            post = Post.objects.get(id=post_id)
            authors = [author.as_json() for author in post.likes.all()]

            response = {
                "type:": "likes",
                "items": authors
            }

        except Exception as e:
            logger.error(e, exc_info=True)
            return HttpResponseServerError()

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class PostCommentsView(View):
    '''
        HANDLE Comment GET and POST
    '''

    def get(self, request, author_id, post_id):
        # Send all comments
        try:
            comments = Comment.objects.filter(
                post=post_id).order_by('-pub_date')

            page = request.GET.get("page")
            size = request.GET.get("size")

            commentsList = []
            for comment in comments:
                # add comment to list
                commentsList.append({
                    "type": "comment",
                    "author": comment.author.as_json(),
                    "comment": comment.comment,
                    "contentType": "text/markdown",
                    "published": comment.pub_date,
                    "id": f"http://{HOST}/{API_PREFIX}author/{author_id}/posts/{comment.post.id}/comments/{comment.id}",
                })

            response = {
                "type": "comments",
                "page": 1,
                "size": 5,
                "post": f"http://{HOST}/{API_PREFIX}/author/{author_id}/posts/{post_id}",
                "id": f"http://{HOST}/{API_PREFIX}/author/{author_id}/posts/{post_id}/comments",
                "comments": commentsList
            }

        except Exception as e:
            logger.error(e, exc_info=True)
            return HttpResponseServerError()

        return JsonResponse(response)

    def post(self, request, author_id, post_id):
        # check if authenticated
        if (not request.user):
            return HttpResponseForbidden()

        comment = request.POST.get('comment')

        # check if empty
        if not len(comment):
            return HttpResponseBadRequest("Comment cannot be empty.")

        pub_date = datetime.now(timezone.utc)

        try:
            author = get_object_or_404(Author, pk=author_id)
            post = get_object_or_404(Post, id=post_id)

            comment = Comment.objects.create(
                author=author,
                post=post,
                comment=comment,
                content_type='PL',  # TODO: add content type
                pub_date=pub_date,
            )

        except Exception:
            return HttpResponse('Internal Server Error')

        return redirect('socialDistribution:commentPost', id=post_id)


@method_decorator(csrf_exempt, name='dispatch')
class CommentLikesView(View):

    def get(self, request, author_id, post_id, comment_id):
        return HttpResponse("This is the authors/aid/posts/pid/comments/cid/likes/ endpoint")


@method_decorator(csrf_exempt, name='dispatch')
class InboxView(View):

    @method_decorator(authenticate_request)
    def get(self, request, author_id):
        """ GET - If authenticated, get a list of posts sent to {author_id} """

        return JsonResponse({
            "message": f"This is the inbox for author_id={author_id}. Only author {author_id} can read this."
        })

    # TODO: authenticate user
    def post(self, request, author_id):
        """ POST - Send a post to {author_id}
            - if the type is “post” then add that post to the author’s inbox
            - if the type is “follow” then add that follow is added to the author’s inbox to approve later
            - if the type is “like” then add that like to the author’s inbox    
        """
        data = json.loads(request.body)
        try:
            if data["type"] == "post":
                return HttpResponse(status=501)  # not implemented

            elif data["type"] == "follow":
                actor, obj = data["actor"], data["object"]
                # actor want's to follow object
                # need to add actor URL to object's inbox
                # object decides later to add actor URL to its outward feed (followers)
                # demo, try with spec sample data
                response_data = str(data["actor"]) + "\n" + str(data["object"])
                return HttpResponse(response_data)  # okay

            elif data["type"] == "like":
                # https://www.youtube.com/watch?v=VoWw1Y5qqt8 - Abhishek Verma
                try:
                    postId = data["object"].split("/")[-1]
                    likingAuthorId = data["author"]["id"].split("/")[-1]
                    post = get_object_or_404(Post, id=postId)
                    author = Author.objects.get(id=likingAuthorId)
                    if post.likes.filter(id=author.id).exists():
                        post.likes.remove(author)
                    else:
                        post.likes.add(author)

                except Exception:
                    return HttpResponse('Internal Server Error')

                return HttpResponse(status=200)

            else:
                return HttpResponseBadRequest()

        except KeyError:
            return HttpResponseBadRequest()

    def delete(self, request, author_id):
        """ DELETE - Clear the inbox """

        return HttpResponse("Hello")

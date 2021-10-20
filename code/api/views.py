from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json

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


def index(request):
    return HttpResponse("Welcome to the Social Distribution API")


@method_decorator(csrf_exempt, name='dispatch')
class AuthorsView(View):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        """ GET - Retrieve all user profiles """

        page = request.GET.get("page")
        size = request.GET.get("size")

        data = []
        for author in Author.objects.all():
            data.append(
                {
                    "type": "author",
                    "id": f"{HOST}{API_PREFIX}authors/{author.id}/",
                    "url": f"{HOST}{API_PREFIX}authors/{author.id}/",
                    "host": f"{HOST}",
                    "displayName": author.displayName,
                    "github": author.githubUrl,
                    "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
                }
            )

        response = {
            "type": "authors",
            "items": data
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorView(View):

    def get(self, request, author_id):
        """ GET - Retrieve profile of {author_id} """

        author = get_object_or_404(Author, pk=author_id)
        response = {
            "type": "author",
            "id": f"{HOST}{API_PREFIX}authors/{author.id}/",
            "url": f"{HOST}{API_PREFIX}authors/{author.id}/",
            "host": f"{HOST}",
            "displayName": author.displayName,
            "github": author.githubUrl,
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
        }
        return JsonResponse(response)

    def post(self, request, author_id):
        """ POST - Update profile of {author_id} """
        return HttpResponse("authors post\nupdate profile")


@method_decorator(csrf_exempt, name='dispatch')
class FollowersView(View):

    def get(self, request, author_id):
        """ GET - Get a list of authors who are the followers of {author_id} """

        author = get_object_or_404(Author, pk=author_id)
        followers = []
        for follower in author.followers.all():
            followers.append({
                "type": "author",
                "id": f"{HOST}{API_PREFIX}authors/{follower.id}/",
                "url": f"{HOST}{API_PREFIX}authors/{follower.id}/",
                "host": f"{HOST}",
                "displayName": follower.displayName,
                "github": follower.githubUrl,
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
            })

        response = {
            "type": "followers",
            "items": followers
        }

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class LikedView(View):

    def get(self, request, author_id):
        return HttpResponse("This is the authors/aid/liked/ endpoint")


@method_decorator(csrf_exempt, name='dispatch')
class PostView(View):

    def get(self, request, author_id, post_id):
        return HttpResponse("This is the authors/aid/posts/pid/ endpoint")


@method_decorator(csrf_exempt, name='dispatch')
class PostLikesView(View):

    def get(self, request, author_id, post_id):
        return HttpResponse("This is the authors/aid/posts/pid/likes/ endpoint")


@method_decorator(csrf_exempt, name='dispatch')
class PostCommentsView(View):

    def get(self, request, author_id, post_id):
        return HttpResponse("This is the authors/aid/posts/pid/comments/ endpoint")


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
                return HttpResponse(status=501)  # not implemented

            else:
                return HttpResponseBadRequest()

        except KeyError:
            return HttpResponseBadRequest()


    def delete(self, request, author_id):
        """ DELETE - Clear the inbox """

        return HttpResponse("Hello")

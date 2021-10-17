from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from socialDistribution.models import *

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
        page = request.GET.get("page")
        size = request.GET.get("size")

        data = []
        for author in Author.objects.all():
            data.append(
                {
                    # WARNING: hardcode
                    "type": "author",
                    "id": f"http://127.0.0.1:8000/authors/{author.id}",
                    "url": f"http://127.0.0.1:8000/authors/{author.id}",
                    "host": "http://127.0.0.1:8000/",
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
        author = get_object_or_404(Author, pk=author_id)
        response = {
            # WARNING; hardcode
            "type": "author",
            "id": f"http://127.0.0.1:8000/authors/{author.id}",
            "url": f"http://127.0.0.1:8000/authors/{author.id}",
            "host": "http://127.0.0.1:8000/",
            "displayName": author.displayName,
            "github": author.githubUrl,
            "profileImage": "https://i.imgur.com/k7XVwpB.jpeg",
        }
        return JsonResponse(response)

    def post(self, request, author_id):
        return HttpResponse("authors post\nupdate profile")


@method_decorator(csrf_exempt, name='dispatch')
class FollowersView(View):

    def get(self, request, author_id):
        return HttpResponse("This is the authors/aid/followers/ endpoint")


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

    def get(self, request, author_id):
        return HttpResponse("This is the authors/aid/inbox/ endpoint")

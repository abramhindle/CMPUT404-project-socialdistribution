import json
from functools import partial

from author import serializers
from author.models import Author, Follow, Inbox
from author.serializers import AuthorSerializer
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.paginator import (EmptyPage, InvalidPage, PageNotAnInteger,
                                   Paginator)
from django.db.models import Subquery
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods
from post.models import Comment, Like, Post
from post.serializers import CommentSerializer, LikeSerializer, PostSerializer
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from server.models import Setting

# Create your views here.


class feed(APIView):
    def get(self, request):
        '''
        GET paginated posts from all authors.
        If the user is authorized, include posts that they are allowed to see.
        If the user is not authorized, only show public listed posts.
        '''
        allPosts = Post.objects.filter(isPublic=True, isListed=True).order_by("-date")

        try:
            size = int(request.query_params.get("size", 5))  # 5 is default right?
            page = int(request.query_params.get("page", 1))  # By default, 1 object per page.
            postPaginator = Paginator(allPosts, size)
        except:
            return Response("Bad request. Invalid parameters.", status=400)
        try:
            serializer = PostSerializer(postPaginator.page(page), many=True)
            pageData = serializer.data
        except InvalidPage:
            pageData = []
        response = {'type': 'posts', 'page': page, 'size': size, 'items': pageData}
        return Response(response)

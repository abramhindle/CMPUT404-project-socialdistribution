from rest_framework import views, status
from rest_framework.response import Response
#import requests
from django.http import Http404
from posts.models import User, Follow, Post, Comment, Category, FollowRequest
from posts.serializers import UserSerializer, PostSerializer, CommentSerializer,FollowSerializer, FollowRequestSerializer
# import requests
from django.http import Http404
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import loader
from preferences import preferences
import commonmark
from posts.helpers import are_friends,get_friends,are_FOAF

class FrontEndPublicPosts(TemplateView):
    def get_posts(self):
        try:
            return Post.objects.filter(visibility='PUBLIC')
        except Post.DoesNotExist:
            raise Http404

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_feed(self):
        # f_level is a list of either ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts()
        return allPosts

    def get(self, request):
        # get the allowedVisibilitys of the relationship between request.user ~ authorid
        user = request.user
        posts = self.get_feed()
        serializer = PostSerializer(posts, many=True)
        contentTypes = []
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            else:
                contentTypes.append( "<p>" + post.content +"</p>")
        return render(request, 'post/public_posts.html', context={ 'posts':serializer.data, 'contentTypes':contentTypes})

class FrontEndAuthorPosts(TemplateView):
    def get_posts(self,author):
        try:
            return Post.objects.filter(author = author)
        except Post.DoesNotExist:
            raise Http404

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_feed(self,user,other,f_level):
        # f_level is a list of either ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts(other)
        feedPosts = allPosts.filter(visibility__in=['PUBLIC','SERVERONLY'])
        allPosts = allPosts.exclude(visibility__in=['PUBLIC','SERVERONLY'])
        for level in f_level:
            feedPosts = feedPosts.union(allPosts.filter(visibility=level))
        allPosts = allPosts.filter(visibility='PRIVATE')
        return feedPosts
        
        # add all posts with acceptable friendship

    def get_friendship_level(self,request,other):
        # TODO: Implement proper friendship checking!

        if(are_friends(request.user,other)):
            return ['FRIENDS', 'FOAF']
        if(are_FOAF(request.user,other)):
            return ['FOAF']
        return []

    def get(self, request, authorid):
        # get the allowedVisibilitys of the relationship between request.user ~ authorid
        author = self.get_user(authorid)
        user = request.user
        friendship_level = self.get_friendship_level(request,author)
        posts = self.get_feed(user,author, friendship_level)
        serializer = PostSerializer(posts, many=True)
        contentTypes = []
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            else:
                contentTypes.append( "<p>" + post.content +"</p>")
        return render(request, 'author/author_posts.html', context={'author': author, 'posts':serializer.data, 'contentTypes':contentTypes})
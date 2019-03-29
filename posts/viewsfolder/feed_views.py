from posts.models import User, Post
from posts.serializers import PostSerializer
from rest_framework import views
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
import commonmark
from posts.helpers import are_friends, get_friends, are_FOAF, get_follow, get_friendship_level, visible_to
from posts.pagination import CustomPagination



class FrontEndPublicPosts(TemplateView):
    def get_posts(self):
        try:
            return Post.objects.filter(visibility='PUBLIC').order_by("-published")
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
        user = request.user
        # userpk = user.pk
        posts = self.get_feed()
        serializer = PostSerializer(posts, many=True)
        contentTypes = []
        # print(user)
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            else:
                contentTypes.append("<p>" + post.content + "</p>")
        return render(request, 'post/feed-posts.html',
                      context={'user_id': user.pk, 'posts': serializer.data, 'contentTypes': contentTypes})


class FrontEndAuthorPosts(TemplateView):
    def get_posts(self,author):
        try:
            return Post.objects.filter(author=author).order_by("-published")
        except Post.DoesNotExist:
            raise Http404

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_feed(self,user,author):
        # f_level is a list of  ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts(author)
        feedPosts=[]
        for post in list(allPosts):
            if(visible_to(post,user)):
                feedPosts.append(post.id)
        return Post.objects.filter(id__in=feedPosts)
        
    def get(self, request, authorid):
        # get the allowedVisibilitys of the relationship between request.user ~ authorid
        author = self.get_user(authorid)
        user = request.user
        friends = are_friends(user, author)
        follow = get_follow(user, author)
        posts = self.get_feed(user, author)
        serializer = PostSerializer(posts, many=True)
        contentTypes = []
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            else:
                contentTypes.append( "<p>" + post.content +"</p>")
        return render(request, 'author/author_posts.html', context={'author': author, 'posts': serializer.data,
                                                                    'contentTypes': contentTypes,
                                                                    'friends': friends,
                                                                    'follow': follow})

class GetAuthorPosts(views.APIView):
    authorHelper = FrontEndAuthorPosts()

    def get(self, request, authorid):
        paginator = CustomPagination()
        author = self.authorHelper.get_user(authorid)
        user = request.user
        posts = self.authorHelper.get_feed(user, author)
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data, "posts")

class FrontEndFeed(TemplateView):
    def get_posts(self):
        try:
            return Post.objects.all()
        except Post.DoesNotExist:
            raise Http404

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_feed(self,user):
        # f_level is a list of  ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts()
        feedPosts=[]
        for post in list(allPosts):
            if(visible_to(post,user)):
                feedPosts.append(post.id)
        return Post.objects.filter(id__in=feedPosts).order_by("-published")

    def get(self, request):
        user = request.user
        posts = self.get_feed(user)
        serializer = PostSerializer(posts, many=True)
        contentTypes = []
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            else:
                contentTypes.append( "<p>" + post.content +"</p>")

        return render(request, 'post/feed-posts.html',
                      context={'author_id': user.pk, 'posts': serializer.data, 'contentTypes': contentTypes})

class UpdateGithubId(TemplateView):
    def post(self, request):
        user = request.user
        newId = request.POST['newId']

        user = User.objects.get(id=user.id)
        user.githubLastId = newId
        user.save()

        return HttpResponse(status=204)



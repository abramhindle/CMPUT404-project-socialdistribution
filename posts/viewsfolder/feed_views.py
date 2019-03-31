from posts.models import User, Post, WWUser
from posts.serializers import PostSerializer
from posts.helpers import get_follow, get_local_user
from posts.helpers import are_friends, are_FOAF, get_user, get_external_posts
from posts.serializers import UserSerializer
from rest_framework import views, status
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
import commonmark
from posts.helpers import are_friends, get_friends, are_FOAF, get_follow, get_friendship_level, visible_to, get_post, \
    get_external_friends, try_get_viewer
from posts.pagination import CustomPagination
from preferences import preferences
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from django.utils.html import escape



class FrontEndPublicPosts(TemplateView):

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
        posts = self.get_feed()
        serializer = PostSerializer(posts, many=True)
        contentTypes = []
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            else:
                contentTypes.append("<p>" + escape(post.content) + "</p>")
        return render(request, 'post/public-make-post.html',
                      context={'user_id': user.pk, 'posts': serializer.data, 'contentTypes': contentTypes,
                               'author_id': user.pk})


class FrontEndAuthorPosts(TemplateView):
    def get_posts(self, author):
        try:
            return Post.objects.filter(author=author)
        except Post.DoesNotExist:
            raise Http404


    def get_feed(self, user, author):
        # f_level is a list of  ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts(author)
        feedPosts = []
        for post in list(allPosts):
            if (visible_to(post, user)):
                feedPosts.append(post.id)
        return Post.objects.filter(id__in=feedPosts)
        
        # add all posts with acceptable friendship

    def get_friendship_level(self, user, other):

        if (are_friends(user, other)):
            return ['FRIENDS', 'FOAF']
        if (are_FOAF(user, other)):
            return ['FOAF']
        return []

    @method_decorator(login_required)
    def get(self, request, authorid):
        # get the allowedVisibilitys of the relationship between request.user ~ authorid
        author = get_user(authorid)
        try:
            local_author = User.objects.get(pk=authorid)
        except:
            local_author = False


        if author == None:
            raise Http404
        user = request.user
        author_serialized = UserSerializer(instance=author)
        user_serialized = UserSerializer(instance=user)
        ww_user = WWUser.objects.get(user_id=user.id)
        ww_author = WWUser.objects.get(user_id=author.id)
        friends = are_friends(ww_user, ww_author)
        follow = get_follow(ww_user, ww_author)
        if local_author:
            posts = self.get_feed(user, author)
            serializer = PostSerializer(posts, many=True)

        else:
            posts = get_external_posts(author, user)
            serializer = PostSerializer(posts, many=True)

        contentTypes = []
        if author.host[-1] == '/':
            author_url = author.host[:-1] + '/author/' + str(author.id)
        else:
            author_url = author.host + '/author/' + str(author.id)
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            else:
                contentTypes.append("<p>" + post.content + "</p>")
        return render(request, 'author/author_posts.html', context={'author': author, 'posts': serializer.data,
                                                                    'contentTypes': contentTypes,
                                                                    'friends': friends,
                                                                    'follow': follow,
                                                                    'user_serialized': user_serialized.data,
                                                                    'author_serialized': author_serialized.data,
                                                                    'author_url': author_url
                                                                    })


class GetAuthorPosts(views.APIView):
    authorHelper = FrontEndAuthorPosts()

    @method_decorator(login_required)
    def get(self, request, authorid):
        paginator = CustomPagination()
        author = get_local_user(authorid)
        if author is None:
            raise Http404
        external_header = request.META.get('HTTP_X_REQUEST_USER_ID', False)
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        if not external_header:
            user = request.user
            friendship_level = self.authorHelper.get_friendship_level(request, author)
            posts = self.authorHelper.get_feed(user, author, friendship_level)
            result_page = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True)
        else:
            if external_header[-1] == '/':
                friend_check_url = external_header + 'friends/'
            else:
                friend_check_url = external_header + '/friends/'
            external_friends = get_external_friends(friend_check_url)
            author_serialized = UserSerializer(instance=author)

            # know they are friends

            posts = Post.objects.filter(author=authorid).exclude(unlisted=True)
            if not serve_images:
                posts.exclude(contentType__in=['img/png;base64', 'image/jpeg;base64'])

            feed = posts.filter(visibility="PUBLIC")
            # check visibility

            if author_serialized.data.get('url') in external_friends:
                feed = feed.union(posts.filter(visibility="FRIENDS"))
            private_access = []
            for post in posts.filter(visibility='PRIVATE'):
                if try_get_viewer(post, external_header):
                    private_access.append(post.id)
            private_access = posts.filter(id__in=private_access)
            feed.union(private_access)
            result_page = paginator.paginate_queryset(feed, request)
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

    def get_feed(self, user):
        # f_level is a list of  ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts()
        feedPosts = []
        for post in list(allPosts):
            if (visible_to(post, user)):
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
                contentTypes.append("<p>" + escape(post.content) + "</p>")

        return render(request, 'post/feed-posts.html',
                      context={'author_id': user.pk, 'posts': serializer.data, 'contentTypes': contentTypes})


class UpdateGithubId(views.APIView):
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        newId = request.data['id']
        print(newId)

        user = User.objects.get(id=user.id)
        user.githubLastId = newId
        user.save()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# TODO THIS
# todo this
class BackEndFeed(views.APIView):
    def get(self, request):
        paginator = CustomPagination()
        # Since we will not be using our api going to use the preferences as a determiner for this.
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        posts = get_posts(serve_images)

        result_page = paginator.paginate_queryset(post, request)

        # Since we will not be using our api going to use the preferences as a determiner for this.
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        if not serve_images and post_model.contentType in ['img/png;base64', 'image/jpeg;base64']:
            raise PermissionDenied

        serializer = PostSerializer(result_page, many=True)
        external_header = request.META.get('HTTP_X_REQUEST_USER_ID', False)
        if external_header:
            vis = visible_to(post_model, external_header, True, False)
        else:
            vis = visible_to(post_model, request.user, True, True)
        if vis:
            return Response(serializer.data)

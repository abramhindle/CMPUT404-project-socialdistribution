from posts.models import Follow
from posts.models import User, Post, WWUser
from posts.serializers import PostSerializer
from posts.helpers import get_external_author_posts, get_user
from posts.helpers import mr_worldwide
from posts.serializers import UserSerializer
from rest_framework import views, status
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
import commonmark
from posts.helpers import are_friends, get_follow, get_friendship_level, visible_to, get_or_create_ww_user, get_ww_user, get_ext_foaf
from posts.helpers import get_or_create_external_header
from posts.helpers import are_friends, get_follow, get_friendship_level, visible_to, get_or_create_ww_user, get_ww_user
from posts.helpers import get_or_create_external_header, get_external_feed
from posts.pagination import CustomPagination
from preferences import preferences
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from django.utils.html import escape
from dispersal.settings import SITE_URL



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
        # The Idea
        # although not bothering with defining source and origin idk
        # (1) get our local posts: source == us, origin == us
        # (2) for each server s we communicated with:
        #           get all public posts they have (including servers they communicate with)
        #           for each post p they give us:
        #               p.source <- s
        #               p.origin == p.origin (ie DO NOT CHANGE IT)
        # (3) serve back all the above posts to the original requester
        user = request.user

        # serve_images = preferences.SitePreferences.serve_others_images
        # if serve_images:
        #     local_posts = Post.objects.filter(visibility='PUBLIC').order_by("-published")
        # else:
        #     local_posts = Post.objects.filter(visibility='PUBLIC').exclude(
        #         contentType__in=['img/png;base64', 'image/jpeg;base64'])

        local_posts = Post.objects.filter(visibility='PUBLIC').filter(unlisted=False).order_by("-published")

        local_posts_list = list(local_posts)
        # NOTE: not necessarily false but assuming false for now
        # TODO: do I need to filter out image posts based on site preferences for mr worldwide too? because rn its not
        worldwide_posts_list = mr_worldwide(user, False)
        posts = local_posts_list + worldwide_posts_list

        serializer = PostSerializer(posts, many=True)
        image_types = ['image/png;base64', 'image/jpeg;base64']
        contentTypes = []
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            elif (post.contentType in image_types):
                try:
                    base64 = post.content.split(',')[1]
                except:
                    base64 = post.content
                contentTypes.append("<img class=\"post-image\"src=\"data:{}, {}\" />".format(post.contentType, base64))
            else:
                contentTypes.append("<p>" + escape(post.content) + "</p>")
        return render(request, 'post/public-posts.html',
                      context={'user_id': user.pk, 'posts': serializer.data, 'contentTypes': contentTypes,
                               'author_id': user.pk, 'cur_site':SITE_URL})


class FrontEndAuthorPosts(TemplateView):
    def get_posts(self, author):
        try:
            return Post.objects.filter(author=author).order_by("-published")
        except Post.DoesNotExist:
            raise Http404


    def get_feed(self, user, author):
        # f_level is a list of  ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts(author)
        feedPosts = []
        ww_user = get_ww_user(user.id)
        ww_author = get_ww_user(author.id)
        f_level = get_friendship_level(ww_user, ww_author)
        for post in list(allPosts):
            if visible_to(post, ww_user):
                feedPosts.append(post.id)
        return Post.objects.filter(id__in=feedPosts).filter(unlisted=False)

        # add all posts with acceptable friendship

    @method_decorator(login_required)
    def get(self, request, authorid):
        # get the allowedVisibilitys of the relationship between request.user ~ authorid
        author = get_user(authorid)
        try:
            local_author = User.objects.get(pk=authorid)
        except:
            local_author = False
        if author is None:
            raise Http404
        user = request.user
        author_serialized = UserSerializer(instance=author)
        user_serialized = UserSerializer(instance=user)
        ww_user = get_or_create_ww_user(user)
        ww_author = get_or_create_ww_user(author)
        friends = False
        follow = get_follow(follower=ww_user, followee=ww_author)

        if local_author:
            posts = self.get_feed(user, author)
            friends = are_friends(ww_user, ww_author)

        else:

            allPosts = get_external_author_posts(author=author, requestor=user)
            posts=[]
            # if the user is local we must verify on our end that they are friends!
            if ww_user.local:
                if follow:
                    foaf=True
                else:
                    foaf = get_ext_foaf(local_user=ww_user,ext_user=ww_author)
                for post in allPosts:
                    if post.visibility=="FRIENDS" and follow:
                        friends = True
                        posts.append(post)
                    elif post.visibility=="FOAF" and foaf:
                        posts.append(post)
                    elif not(post.visibility in ["FRIENDS","FOAF"]):
                        posts.append(post)
            else:
                posts = allPosts

        serializer = PostSerializer(posts, many=True)
        image_types = ['image/png;base64', 'image/jpeg;base64']
        contentTypes = []
        if author.host[-1] == '/':
            author_url = author.host[:-1] + '/author/' + str(author.id)
        else:
            author_url = author.host + '/author/' + str(author.id)
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            elif (post.contentType in image_types):
                try:
                    base64 = post.content.split(',')[1]
                except:
                    base64 = post.content
                contentTypes.append("<img class=\"post-image\"src=\"data:{}, {}\" />".format(post.contentType, base64))
            else:
                contentTypes.append("<p>" + escape(post.content) + "</p>")
        return render(request, 'author/author_posts.html', context={'author': author,
                                                                    'author_id': user.id,
                                                                    'posts': serializer.data,
                                                                    'contentTypes': contentTypes,
                                                                    'friends': friends,
                                                                    'follow': follow,
                                                                    'user_serialized': user_serialized.data,
                                                                    'author_serialized': author_serialized.data,
                                                                    'author_url': author_url,
                                                                    'cur_site':SITE_URL
                                                                    })

class GetAuthorPosts(views.APIView):
    authorHelper = FrontEndAuthorPosts()

    @method_decorator(login_required)
    def get(self, request, authorid):
        paginator = CustomPagination()
        try:
            author = User.objects.get(pk=authorid)
        except:
            author = None
        if author is None:
            raise Http404
        external_header = request.META.get('HTTP_X_REQUEST_USER_ID', False)
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        if not external_header:
            user = request.user
            posts = self.authorHelper.get_feed(user, author)
            result_page = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True)
        else:
            user_id = external_header.split('/author/')[1]
            if user_id[-1] == '/':
                user_id = user_id[:-1]
            ww_user = get_or_create_external_header(external_header)
            ww_author = get_or_create_ww_user(author)
            try:
                follow = Follow.objects.get(followee=ww_user, follower=ww_author)
            except:
                follow = False
            if follow:
                foaf= True
            else:
                foaf = get_ext_foaf(local_user=ww_author, ext_user=ww_user)

            allPosts = self.authorHelper.get_posts(author=author)
            posts = []
            # if the user is local we must verify on our end that they are friends!
            if ww_user.local:
                for post in allPosts:
                    if post.visibility == "FRIENDS" and follow:
                        posts.append(post.id)
                    elif (post.visibility == "FOAF" and foaf):
                        posts.append(post.id)
                    elif not (post.visibility in ["FRIEND","FOAF"]):
                        posts.append(post.id)
            else:
                posts = allPosts
            if len(posts) == 0:
                posts = Post.objects.none()
            else:
                posts = Post.objects.filter(id__in=posts)
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
        except:
            raise Http404

    def get_feed(self, user):
        # f_level is a list of  ['FOAF'] or ['FOAF','FRIENDS'] or []
        allPosts = self.get_posts()
        feedPosts = []
        ww_user = get_ww_user(user.id)
        for post in list(allPosts):
            if visible_to(post, ww_user):
                feedPosts.append(post.id)
        return Post.objects.filter(id__in=feedPosts).order_by("-published")

    def get(self, request):
        user = request.user
        local_posts_list = list(self.get_feed(user))
        ext_posts = get_external_feed(user)
        posts = local_posts_list + ext_posts
        serializer = PostSerializer(posts, many=True)
        contentTypes = []
        image_types = ['image/png;base64', 'image/jpeg;base64']
        for post in posts:
            if post.contentType == "text/markdown":
                contentTypes.append(commonmark.commonmark(post.content))
            elif (post.contentType in image_types):
                try:
                    base64 = post.content.split(',')[1]
                except:
                    base64 = post.content
                contentTypes.append("<img class=\"post-image\"src=\"data:{}, {}\" />".format(post.contentType, base64))
            else:
                contentTypes.append("<p>" + escape(post.content) + "</p>")

        return render(request, 'post/feed-posts.html',
                      context={'author_id': user.pk, 'posts': serializer.data, 'contentTypes': contentTypes, 'cur_site':SITE_URL})


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


class BackEndFeed(views.APIView):

    def get_posts(self):
        return Post.objects.filter(unlisted=False).order_by("-published")

    def get(self, request):
        paginator = CustomPagination()
        # Since we will not be using our api going to use the preferences as a determiner for this.
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        external_header = request.META.get('HTTP_X_REQUEST_USER_ID', False)
        if external_header != False:
            requestor = \
                WWUser.objects.get_or_create(url=external_header, user_id=external_header.split('/author/')[1])[0]
        else:
            requestor = get_ww_user(request.user.id)

        posts = self.get_posts()
        posts_list = []
        for post in posts:
            if visible_to(post, requestor, False, external_header == False):
                posts_list.append(post.id)
        if len(posts_list) == 0:
            posts_list = Post.objects.none()
        else:
            posts_list = Post.objects.filter(id__in=posts_list)
        result_page = paginator.paginate_queryset(posts_list, request)


        serializer = PostSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data, "posts")

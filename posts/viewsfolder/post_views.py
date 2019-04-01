import commonmark
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.http.response import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from preferences import preferences
from rest_framework import views, status
from rest_framework.response import Response
from posts.helpers import are_FOAF, visible_to, get_post, get_ww_user, parse_id_from_url, get_local_post
from posts.helpers import mr_worldwide
from posts.helpers import parse_host_from_url
from posts.models import Category, Viewer, Post, User, WWUser
from posts.pagination import CustomPagination
from posts.serializers import PostSerializer, UserSerializer
from django.utils.html import escape

class PostView(views.APIView):
    @method_decorator(login_required)
    def post(self, request):
        """
        Create new categories
        """
        if not request.user.approved:
            raise PermissionDenied

        # handle form data for categories
        if type(request.data) is dict:
            categories = request.data.get("categories")
            visibleTo = request.data.get("visibleTo")
        else:
            categories = request.data.getlist("categories")
            visibleTo = request.data.getlist("visibleTo")

        try:
            with transaction.atomic():
                if categories is not None:
                    # author has defined categories
                    for cat in categories:
                        cat_obj = Category.objects.get_or_create(category=cat)
                serializer = PostSerializer(data=request.data, context={'user': request.user})
                if serializer.is_valid():
                    post = serializer.save()
                else:
                    raise ValidationError
                if visibleTo is not None:
                    # author has defined visibleTo
                    for viewer in visibleTo:
                        Viewer.objects.get_or_create(url=viewer, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required)
    def get(self, request):
        paginator = CustomPagination()
        # Since we will not be using our api going to use the preferences as a determiner for this.
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied

        local_posts = Post.objects.filter(visibility='PUBLIC').order_by("-published").exclude(
            unlisted=True
        )

        result_page = paginator.paginate_queryset(local_posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data, "posts")


class PostCreateView(TemplateView):
    def get(self, request):
        serializer = PostSerializer()
        return render(request, "makepost/make-post.html", context={"serializer": serializer})


class PostViewID(views.APIView):

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_post(self, pk):
        try:
            return Post.objects.filter(pk=pk)
        except:
            raise Http404

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, pk):
        paginator = CustomPagination()
        post = self.get_post(pk)
        if post.count() != 1:
            raise Http404
        post_model = post.first()
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
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk):
        paginator = CustomPagination()
        post = self.get_post(pk)
        # Since we will not be using our api going to use the preferences as a determiner for this.
        if post.count() != 1:
            raise Http404
        post_model = post.first()
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        if not serve_images and post_model.contentType in ['img/png;base64', 'image/jpeg;base64']:
            raise PermissionDenied
        result_page = paginator.paginate_queryset(post, request)
        serializer = PostSerializer(result_page, many=True)
        requestor_author = request.data.get('author')
        ww_requestor = \
            WWUser.objects.get_or_create(url=requestor_author['id'], user_id=parse_id_from_url(requestor_author['id']))[
                0]
        ww_post_author = WWUser.objects.get(user_id=post_model.author_id)
        # YES, this doesn't make yes.
        # BLAME THE API
        if post_model.visibility == 'PUBLIC':
            return Response(data=serializer.data)
        # TODO Come back after new friend stuff
        # Come https://github.com/dispersal/CMPUT404-project-socialdistribution/blob/b042afa3f0bb21307f96c4efecf2fc5a594f264f/example-article.json#L260
        if post_model.visibility == 'PRIVATE':
            viewing = Viewer.objects.filter(post=post, url=requestor_author.get('url', ''))
            if len(viewing) > 0:
                return Response(data=serializer.data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        if (post_model.visibility in "FOAF"):
            authorid = post_model.author.id
            user = request.user
            other = self.get_user(authorid)
            if (are_FOAF(ww_requestor, ww_post_author)):
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        post = get_local_post(pk)
        newPostSerializer = PostSerializer(post, data=request.data, context={"user": request.user}, partial=True)
        if newPostSerializer.is_valid():
            newPostSerializer.save()
            return Response(newPostSerializer.data, status=status.HTTP_201_CREATED)
        return Response(newPostSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required)
    def delete(self, request, pk):

        # request.user
        post = self.get_post(pk)
        if post.count() != 1:
            Response(status=status.HTTP_204_NO_CONTENT)
        post_obj = post.first()
        if post_obj.author == request.user:
            post = self.get_post(pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FrontEndPostViewID(TemplateView):

    def get(self, request, pk):
        post, comments = get_post(pk, request.user)
        if post is None:
            raise Http404
        serializer = PostSerializer(instance=post)
        if comments is None:
            comments = serializer.data.get("comments", [])
        poster = UserSerializer(instance=post.author)
        loggedIn = request.user
        owns_post = (poster.data.get('id') == loggedIn.id)
        image_types = ['image/png;base64', 'image/jpeg;base64']
        user_serialized = UserSerializer(instance=request.user)
        if post.contentType == "text/markdown":
            post_content = commonmark.commonmark(post.content)

        elif (post.contentType in image_types):
            try:
                base64 = post.content.split(',')[1]
            except:
                base64 = post.content
            post_content = "<img class=\"post-image\"src=\"data:{}, {}\" />".format(post.contentType, base64)
        else:
            post_content = "<p>" + escape(post.content) + "</p>"

        if visible_to(post, request.user, direct=True):
            return render(request, 'post/post.html', context={'post': serializer.data, 'post_content': post_content,
                                                              'comments': comments,
                                                              "owns_post": owns_post,
                                                              'user_serialized': user_serialized.data})

        raise PermissionDenied

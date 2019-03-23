from django.forms.models import model_to_dict
from rest_framework import views, status
from rest_framework.response import Response
from django.http import Http404, HttpResponseRedirect
from .models import User, Follow, Post, Comment, Category, FollowRequest, Viewer
from .serializers import UserSerializer
from .serializers import PostSerializer
from .serializers import CommentSerializer
from django.http import Http404
from .models import User, Post, Comment, Category
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from preferences import preferences
from .pagination import CustomPagination
from django.views.decorators.csrf import csrf_exempt
import commonmark
from .helpers import are_friends, are_FOAF
from django.db import transaction


class UserView(views.APIView):

    def get_user(self, user):
        try:
            return User.objects.get(pk=user.pk)
        except:
            raise Http404

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'create': True})
        if serializer.is_valid() and request.user.is_anonymous:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required)
    def get(self, request):
        user = self.get_user(request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @method_decorator(login_required)
    def put(self, request):
        user = self.get_user(request.user)
        serializer = UserSerializer(user, data=request.data, partial=True, context={'create':False})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewID(views.APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = UserSerializer(user, context={'request':request})
        return Response(serializer.data)


class AdminUserView(TemplateView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        unapproved = User.objects.filter(approved=False)

        return render(request, 'users/approve_user.html', context={'unapproved': unapproved})

    @method_decorator(login_required)
    def post(self, request):
        if not request.user.is_staff:
            raise PermissionDenied
        user_to_approve = request.POST['user']
        user = User.objects.get(id=user_to_approve)
        user.approved = True
        user.save()
        unapproved = User.objects.filter(approved=False)

        return render(request, 'users/approve_user.html', context={'unapproved': unapproved})


# TODO: (<AUTHENTICATION>) Make sure author is approved

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

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    @method_decorator(login_required)
    def get(self, request):
        paginator = CustomPagination()
        # Since we will not be using our api going to use the preferences as a determiner for this.
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        if serve_images:
            posts = Post.objects.all().order_by("-published")
        else:
            posts = Post.objects.exclude(contentType__in=['img/png;base64', 'image/jpeg;base64'])

        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data, "posts")

class PostCreateView(TemplateView):
    def get(self, request):
        serializer = PostSerializer()
        return render(request, "makepost/posts.html", context={"serializer" : serializer})


class PostCreateView(TemplateView):
    def get(self, request):
        serializer = PostSerializer()
        return render(request, "makepost/posts.html", context={"serializer" : serializer})


class PostViewID(views.APIView):

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, pk):
        post = self.get_post(pk)
        # Since we will not be using our api going to use the preferences as a determiner for this.
        serve_other_servers = preferences.SitePreferences.serve_others_posts
        if not serve_other_servers:
            raise PermissionDenied
        serve_images = preferences.SitePreferences.serve_others_images
        if not serve_images and post.contentType in ['img/png;base64', 'image/jpeg;base64']:
            raise PermissionDenied

        # TODO: can probably remove context
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request, pk):
        post = self.get_post(pk)
        # YES, this doesn't make yes.
        # BLAME THE API
        # print("ASDFSDF")
        if (post.visibility in "FOAF"):
            authorid = post.author.id
            user = request.user
            other = self.get_user(authorid)
            if(are_FOAF(user,other)):
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        # elif post.author == request.user:
        #     print("editing")
        #     serializer = PostSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        post = self.get_post(pk)
        newPostSerializer = PostSerializer(post, data=request.data, context={"user":request.user}, partial=True)
        if newPostSerializer.is_valid():
            newPostSerializer.save()
            return Response(newPostSerializer.data, status=status.HTTP_201_CREATED)
        return Response(newPostSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(login_required)
    def delete(self, request, pk):

        # request.user
        post_obj = self.get_post(pk)
        if post_obj.author == request.user:
            post = self.get_post(pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FrontEndPostViewID(TemplateView):
    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post)
        poster = serializer.data["author"]["id"].replace("-", "")
        loggedIn = request.user.id.hex
        owns_post = poster == loggedIn

        if post.contentType == "text/markdown":
            post_content = commonmark.commonmark(post.content)
        else:
            post_content = "<p>" + post.content + "</p>"

        return render(request, 'post/post.html', context={'post': serializer.data, 'post_content': post_content, 'comments': serializer.data["comments"], "owns_post": owns_post})


class FrontEndUserEditView(TemplateView):

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        user_data = serializer.data
        github_url = user_data['github']
        github_username = github_url.split('/')[-1]
        return render(request, 'users/edit_user.html', context={'user': serializer.data, 'github_username':github_username})


    @method_decorator(login_required)
    def post(self, request):

        user = request.user
        request_serializer = UserSerializer(user)
        i = request_serializer.data
        update = (request.POST).dict()
        for attribute, value in update.items():
            if value != "":
                setattr(user, attribute, value)
        try:
            user.save()
        except:
            github_url = request_serializer.data['github']
            github_username = github_url.split('/')[-1]
            return render(request, 'users/edit_user.html', \
                context={'user': request_serializer.data, 'github_username':github_username,
                'error_message':'Error'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        github_url = serializer.data['github']
        github_username = github_url.split('/')[-1]
        return HttpResponseRedirect(reverse('edit_user'))

class FrontEndAuthorPosts(TemplateView):
    def get_posts(self,author):
        return Post.objects.filter(author = author)

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

class FrontEndAuthorPosts(TemplateView):
    def get_posts(self,author):
        return Post.objects.filter(author = author)

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


class FrontEndAuthorPosts(TemplateView):
    def get_posts(self,author):
        return Post.objects.filter(author = author)

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


class CommentViewList(views.APIView):

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before posting
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def post(self, request, post_id):
        if not request.user.approved:
            raise PermissionDenied
        serializer = CommentSerializer(data=request.data, context={'post_id': post_id, 'user': request.user})
        # print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, post_id):
        paginator = CustomPagination()
        comments = Comment.objects.filter(parent_post_id=post_id).order_by("-published")
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data, "comments")


class FrontEndCommentView(TemplateView):
    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except:
            raise Http404

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request, post_id):
        if not request.user.approved:
            raise PermissionDenied
        post = self.get_post(post_id)
        serializer = PostSerializer(post)
        return render(request, 'post/post.html', context={'post': serializer.data, 'comments': serializer.data["comments"]})

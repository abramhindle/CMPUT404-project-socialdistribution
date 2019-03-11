from rest_framework import views, status
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .models import User, Post, Comment, Category
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import loader
from django.shortcuts import render
# Create your views here.

class UserView(views.APIView):

    def get_user(self, user):
        try:
            return User.objects.get(pk=user.pk)
        except User.DoesNotExist:
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
        categories = request.data.get("categories")
        if categories is not None:
            # author has defined categories
            for cat in categories:
                # check if category exists
                try:
                    cat_obj = Category.objects.get(category=cat)
                except Category.DoesNotExist:
                    cat_obj = None

                if cat_obj is None:
                    Category.objects.create(category=cat)

        serializer = PostSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewID(views.APIView):
    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post)
        return render(request, 'post/post.html', context={'post': serializer.data})

    @method_decorator(login_required)
    def delete(self, request, pk):

        # request.user
        post_obj = Post.objects.get(pk=pk)
        if post_obj.author == request.user:
            post = self.get_post(pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CommentViewList(views.APIView):

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before posting
    # @method_decorator(login_required)
    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data, context={'post_id': post_id, 'user': request.user})
        # print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: (<AUTHENTICATION>, <VISIBILITY>) check VISIBILITY before getting
    def get(self, request, post_id):
        comments = Comment.objects.filter(parent_post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

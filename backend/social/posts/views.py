from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from django.views import generic
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import (
                                        HTMLFormRenderer, 
                                        JSONRenderer, 
                                        BrowsableAPIRenderer,
                                    )

class post_list(APIView):

    def get(self, request, pk_a):
        """
        Get the list of posts on our website
        """
        author = Author.objects.get(id=pk_a)
        posts = Post.objects.filter(author=author)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, pk_a):
        # author = Author.objects.get(id=pk_a)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_posts(request, pk_a):
    """
    Post a question
    """
    author = Author.objects.get(id=pk_a)
    posts = Post.objects.filter(author=author)
    serializer = PostSerializer(posts, data=request.data)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(status=400, data=serializer.errors)

@api_view(['GET'])
def get_comments(request, pk_a, pk):
    """
    Get the list of comments on our website
    """
    author = Author.objects.get(id=pk_a)
    post = Post.objects.get(author=author, id=pk)
    comments = Comment.objects.filter(author=author,post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_likes(request, pk_a, pk):
    """
    Get the list of comments on our website
    """
    author = Author.objects.get(id=pk_a)
    post = Post.objects.get(author=author, id=pk)
    likes = Like.objects.filter(object=post.id)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_posts'

    def get_queryset(self):
        """Return the last five published posts."""
        return Post.objects.order_by('title')[:5]

class DetailView(generic.DetailView):
    model = Post
    context_object_name = 'postt'
    template_name = 'posts/detail.html'
    

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):

    model = Post
    template_name = 'posts/delete.html'
    context_object_name = 'post'
    success_url = '/admin/'
    
    def test_func(self):
        post = self.get_object()
        print(post.title)
        if self.request.user == post.author.user:
            return True
        return False

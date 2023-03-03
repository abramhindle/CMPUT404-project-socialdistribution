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
from .pagination import PostSetPagination
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.renderers import (
                                        HTMLFormRenderer, 
                                        JSONRenderer, 
                                        BrowsableAPIRenderer,
                                    )
import base64
from .image_renderer import JPEGRenderer, PNGRenderer

class post_list(APIView, PageNumberPagination):
    serializer_class = PostSerializer
    pagination_class = PostSetPagination

    def get(self, request, pk_a):
        """
        Get the list of posts on our website
        """
        author = Author.objects.get(id=pk_a)
        posts = Post.objects.filter(author=author)
        posts = self.paginate_queryset(posts, request) 
        serializer = PostSerializer(posts, many=True)
        return  self.get_paginated_response(serializer.data)

    def post(self, request, pk_a):
        pk = str(uuid.uuid4())
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            return Response("Author not found", status=status.HTTP_404_NOT_FOUND)

        # should do this a different fway but for now, it should serialize as image
        if 'image' in request.data['contentType']:
            serializer = ImageSerializer(data=request.data, context={'author_id': pk_a})
        else:
            serializer = PostSerializer(data=request.data, context={'author_id': pk_a})
        
        if serializer.is_valid():
            # using raw create because we need custom id
            # print("original",serializer.validated_data.get('categories'))
            # categories = ' '.join(serializer.validated_data.get('categories'))
            # print("categories", categories)
            #serializer.validated_data.pop('categories')
            serializer.validated_data.pop("author")
            post = Post.objects.create(**serializer.validated_data, author=author, id=pk)
            post.update_fields_with_request(request)

            serializer = PostSerializer(post, many=False)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_comments(request, pk_a, pk):
#     """
#     Get the list of comments on our website
#     """
#     author = Author.objects.get(id=pk_a)
#     post = Post.objects.get(author=author, id=pk)
#     comments = Comment.objects.filter(author=author,post=post)
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def get_likes(request, pk_a, pk):
    """
    Get the list of comments on our website
    """
    post = Post.objects.get(id=pk)
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

class ImageView(APIView):
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a) 
            post = Post.objects.get(author=author, id=pk)
            
            # not image post
            if 'image' not in post.contentType:
                error_msg = {"message":"Post does not contain an image!"}
                return Response(error_msg,status=status.HTTP_404_NOT_FOUND)

            # no image included in post
            if not post.image:
                error_msg = {"message":"Post does not contain an image!"}
                return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
            
            # decode the image
            post_content = post.contentType.split(';')[0]
            image = base64.b64decode(post.content.strip("b'").strip("'"))
            return Response(image, content_type=post_content, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            error_msg = {"message":"Post does not exist!"}
            return Response(error_msg,status=status.HTTP_404_NOT_FOUND)
        
class LikeView(APIView, PageNumberPagination):
    serializer_class = LikeSerializer
    pagination_class = PostSetPagination
    
    def post(self, request, pk_a):
        post_id = uuid.uuid4
        
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        serializer = LikeSerializer(data=request.data, context={'author_id': pk_a})
        if serializer.is_valid():
            # using raw create because we need custom id
            # print("original",serializer.validated_data.get('categories'))
            # categories = ' '.join(serializer.validated_data.get('categories'))
            # print("categories", categories)
            #serializer.validated_data.pop('categories')
            serializer.validated_data.pop("author")
            like = Like.objects.create(**serializer.validated_data, author=author, id=post_id)
            like.update_fields_with_request(request)

            serializer = LikeSerializer(like, many=False)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     author = Author.objects.get(id=pk_a)
        # except Author.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        
        # data = {'author': author.id, **request.data}
        # serializer = LikeSerializer(data=data)
        
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView, PageNumberPagination):
    serializer_class = CommentSerializer
    pagination_class = PostSetPagination

    def get(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
            
        post = Post.objects.get(author=author, id=pk)
        comments = Comment.objects.filter(author=author,post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request,pk_a, pk):
        comment_id = uuid.uuid4
        try:
            author = Author.objects.get(pk=request.data["author_id"])
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        try: 
            post = Post.objects.get(pk=request.data["post_id"])
        except Post.DoesNotExist:
            error_msg = "Post id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)
        
        
        comment = Comment.objects.create(author=author, post=post, id=comment_id, comment=request.data["comment"])
        return Response(status=status.HTTP_200_OK)

        # Able to create the comment but there is an issue with the serializer. 
        # Only implement below when serializer is fixed and working
        # Remove Lines 254 and 255 and uncomment everything below. save 254 and 255 in case not fixed. 

        # serializer = CommentSerializer(data=request.data, context={request.data["author_id"]})
        # if serializer.is_valid():
        #     text = request.data["comment"]
        #     comment = Comment.objects.create(author=author, post=post, id=comment_id, comment=text)
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
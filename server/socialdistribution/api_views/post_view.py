from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import Post, Author
from socialdistribution.serializers import PostSerializer, AuthorSerializer
from socialdistribution.pagination import PostPagination

@api_view(['GET', 'POST'])
def post_view(request, authorID):
    if request.method == "GET":
        # get recent posts of author (paginated)
        paginator = PostPagination()
        posts = Post.objects.filter(authorID=authorID).order_by('-published')
        paginated = paginator.paginate_queryset(posts, request)
        posts_serializer = PostSerializer(paginated, many=True)

        author = get_object_or_404(Author, authorID=authorID)
        author_serializer = AuthorSerializer(author)
        data_copy = posts_serializer.data
        for post in data_copy: # add author data to each post
            del post['authorID']
            del post['postID']
            post['author'] = author_serializer.data

        return paginator.get_paginated_response(data_copy)

    elif request.method == "POST":
        # create a new post
        data = request.data
        data['authorID'] = authorID
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response({"postID":post.postID}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def post_detail_view(request, authorID, postID):
    if request.method == "GET":
        # get post data
        post = get_object_or_404(Post, postID=postID)
        post_serializer = PostSerializer(post)
        # get author data
        author = get_object_or_404(Author, authorID=authorID)
        author_serializer = AuthorSerializer(author)

        data_copy = post_serializer.data
        del data_copy['authorID']
        del data_copy['postID']
        data_copy['author'] = author_serializer.data # add author data to post data
        return Response(data_copy)

    elif request.method == "PUT":
        # create a new post with the given id
        data = request.data
        data['authorID'] = authorID
        data['postID'] = postID

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response({"postID":post.postID}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


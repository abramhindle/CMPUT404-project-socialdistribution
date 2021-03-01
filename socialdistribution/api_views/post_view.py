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
        posts = Post.objects.filter(authorID=authorID, visibility="PUBLIC").order_by('-published')
        paginated = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

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
        serializer = PostSerializer(post)
        return Response(serializer.data)

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
    
    elif request.method == "POST":
        #update the post
        new_data = request.data
        new_data['authorID'] = authorID
        new_data['postID'] = postID
        try:
            mod_post = get_object_or_404(Post, postID=postID)
        except mod_post.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        if mod_post.authorID != authorID:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        serializer = PostSerializer(mod_post, data=new_data)
        if serializer.is_valid():
            post = serializer.save()
            return Response({"postID":post.postID}, status=status.HTTP_200_OK)
        else:
            return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        try:
            del_post = get_object_or_404(Post, postID=postID)
        except del_post.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        operation = del_post.delete()
        if operation:
            return Response({'message': "delete successful!"}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"delete was unsuccessful"}, status=status.HTTP_410_GONE)     
        
        


        


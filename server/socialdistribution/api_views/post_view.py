from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import status
from socialdistribution.models import Post, Author
from socialdistribution.serializers import PostSerializer, AuthorSerializer

@api_view(['GET', 'POST'])
def post_view(request, authorID):
    if request.method == "GET":
        # get recent posts of author (paginated)
        pass
    elif request.method == "POST":
        # create a new post
        data = request.data
        data['authorID'] = authorID
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return JsonResponse({"postID":post.postID}, status=status.HTTP_201_CREATED)
        return JsonResponse({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def post_detail_view(request, authorID, postID):
    if request.method == "GET":
        # get post data
        post = get_object_or_404(Post, postID=postID)
        post_serializer = PostSerializer(post)
        # get author data
        author = get_object_or_404(Author, authorID=authorID)
        author_serializer = AuthorSerializer(author)

        temp = post_serializer.data
        del temp['authorID']
        del temp['postID']
        temp['author'] = author_serializer.data # add author data to post data
        return JsonResponse(temp, safe=False)

    elif request.method == "PUT":
        # create a new post with the given id
        data = request.data
        data['authorID'] = authorID
        data['postID'] = postID

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return JsonResponse({"postID":post.postID}, status=status.HTTP_201_CREATED)
        return JsonResponse({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



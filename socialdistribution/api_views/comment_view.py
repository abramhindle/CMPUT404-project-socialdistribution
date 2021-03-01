from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import Post, Comment
from socialdistribution.serializers import CommentSerializer
from socialdistribution.pagination import CommentPagination

@api_view([ 'GET','POST'])
def comment_view(request, author_write_article_ID, postID):
    if request.method == "GET":
        paginator = CommentPagination()
        comments = Comment.objects.filter(postID=postID).order_by('-published')
        paginated = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        # create a new comment
        data = request.data
        data['author_write_article_ID'] = author_write_article_ID
        data['postID'] = postID
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            # increment comment count in post
            post = Post.objects.get(postID=postID)
            post.count += 1
            post.comment_list.insert(0,serializer.data)
            post.save()
            return Response({"commentID":comment.commentID}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
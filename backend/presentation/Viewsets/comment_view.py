from presentation.models import Author, Follower, Post, Comment
from django.shortcuts import get_object_or_404
from presentation.Serializers.comment_serializer import CommentSerializer
from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse
from . import urlutil

'''
URL: ://service/author/{author_id}/posts/{post_id}/comments access
GET get comments of the post
POST if you post an object of “type”:”comment”, it will add your comment to the post
'''


def getAuthorIDFromRequestURL(request, id):
    host = urlutil.getSafeURL(request.build_absolute_uri())
    author_id = f"{host}/author/{id}"
    return author_id


def getPostIDFromRequestURL(request, id):
    post_id = f"/posts/{id}"
    return post_id


def getCommentIDFromRequestURL(request, id):
    comment_id = f"/comments/{id}"
    return comment_id


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    # GET a list of comments of the post
    def list(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        post_id = getPostIDFromRequestURL(
            request, self.kwargs['post_id'])
        post_id = author_id + post_id
        post = get_object_or_404(Post, id=post_id)
        queryset = Comment.objects.filter(post=post)
        if queryset.exists():
            comments = list(queryset.values())
            # May have mistakes here, do we need to change comment model?
            return JsonResponse(comments, safe=False)
        else:
            Comment.objects.create(post=post)
            return Response({
                'type': 'comment',
                'items': []
            })

    # GET a single comment using comment_id
    def retrieve(self, request, *args, **kwargs):
        comment_id = request.build_absolute_uri()[:-1]
        queryset = Comment.objects.get(id=comment_id)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data)

    # POST a new comment under a post
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        # assume the id of the commmenter is part of the data
        # CHANGE THIS LATER!
        commenter_id = request_data.get('author', None)
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        post_id = getPostIDFromRequestURL(
            request, self.kwargs['post_id'])
        post_id = author_id + post_id
        comment = request_data.get('comment', None)
        content_type = request_data.get('contentType', None)
        # create comment id
        cuuid = str(uuid.uuid4().hex)
        comment_id = f"{post_id}/comments/{cuuid}"
        comment_data = {'type': 'comment', 'author': commenter_id, 'comment': comment, 'contentType': content_type,
                        'post': post_id, 'id': comment_id}
        serializer = self.serializer_class(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        else:
            return Response(serializer.errors,
                            status=400)

    def delete(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        post_id = getPostIDFromRequestURL(
            request, self.kwargs['post_id'])
        post_id = author_id + post_id
        post = get_object_or_404(Post, id=post_id)
        comments = get_object_or_404(Comment, post=post)
        comment_id = getCommentIDFromRequestURL(
            request, self.kwargs['comment_id'])
        comment_id = post_id + comment_id
        comment = get_object_or_404(Comment, id=comment_id)
        # Possible mistake?
        try:
            comment.delete()
        except ValueError:
            return Response("No such a comment. Deletion fails.", 500)
        return Response("Delete successful")

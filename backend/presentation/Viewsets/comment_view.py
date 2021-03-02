from presentation.models import Author, Follower, Post
from django.shortcuts import get_object_or_404
from presentation.Serializers.comment_serializer import CommentSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import uuid
from urllib.parse import urlparse

'''
URL: ://service/author/{author_id}/posts/{post_id}/comments access
GET get comments of the post
POST if you post an object of “type”:”comment”, it will add your comment to the post
'''

'''
Manual Test:
POST:
{"displayName": "Lara Croft","github": "http://github.com/laracroft","username":"LaraCroft","email": "lara@gmail.com","password": "lara1234"}

'''
def getAuthorIDFromRequestURL(request, id):
    parsed_url = urlparse(request.build_absolute_uri())
    host = '{url.scheme}://{url.hostname}:{url.port}'.format(
        url=parsed_url)
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
            comments = Comment.objects.get(post=post)
            # May have mistakes here, do we need to change comment model?
            return Response({
                'type': 'comment',
                'items': comments.items
            })
        else:
            Comment.objects.create(post=post)
            return Response({
                'type': 'comment',
                'items': []
            })    

    # GET a single comment using comment_id
    def retrieve(self, request, *args, **kwargs):
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        post_id = getPostIDFromRequestURL(
            request, self.kwargs['post_id'])
        comment_id = getCommentIDFromRequestURL(
            request, self.kwargs['comment_id'])
        post_id = author_id + post_id
        comment_id = post_id + comment_id
        post = get_object_or_404(Post, id=post_id)
        comments = get_object_or_404(Comment, post=post)
        if comment_id in comments.items:
            # Is there a problem about the response?
            f = get_object_or_404(Comment, id=comment_id)
            return Response({'exist': True})
        else:
            return Response({'exist': False}, 404)

    # POST a new comment under a post
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        # assume the id of the commmenter is part of the data
        # CHANGE THIS LATER!
        commenter_id = request_data.get('commenter', None)
        author = get_object_or_404(Author, id=commenter_id)
        author_id = getAuthorIDFromRequestURL(
            request, self.kwargs['author_id'])
        post_id = getPostIDFromRequestURL(
            request, self.kwargs['post_id'])
        post_id = author_id + post_id
        comment = request_data.get('comment', None)
        content_type = request_data.get('contentType', None)
        published = request_data.get('published', None)
        # create comment id
        cuuid = str(uuid.uuid4().hex)
        comment_id = f"{post_id}/comments/{cuuid}"
        comment_data = {'author': author, 'comment': comment, 'contentType': content_type, 
                        'published': published, 'id': comment_id}

        serializer = self.serializer_class(data=author_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 200)

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
        # Possible mistake?
        try:
            comments.items.remove(comment_id)
            followers.save()
        except ValueError:
            return Response("No such a comment. Deletion fails.", 500)
        return Response("Delete successful")

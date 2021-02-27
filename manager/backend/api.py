from rest_framework.response import Response
from .models import Author, Post
from rest_framework import serializers, viewsets, permissions
from .serializers import AuthorSerializer, PostSerializer

# Author Viewset
class AuthorViewSet(viewsets.ModelViewSet):
    
    queryset = Author.objects.all()

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AuthorSerializer

    lookup_field = 'id'

class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny
    ]

    lookup_field = 'author_id'

    serializer_class = PostSerializer

    queryset = Post.objects.all()

    def list(self, request, author_id=None, id=None, *args, **kwargs):
        if author_id:
            posts = Post.objects.filter(author_id=author_id).order_by('-published')
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, author_id=None, id=None, *args, **kwargs):
        if author_id and id:
            post = Post.objects.filter(id=id)
            serializer = self.get_serializer(post, many=True)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, author_id=None, id=None, *args, **kwargs):
        if author_id and id:
            post = Post.objects.filter(id=id)
            serializer = self.get_serializer(post, many=True)
            deleted_post = serializer.data
            post.delete()
            return Response(deleted_post)
        return super().destroy(request, *args, **kwargs)

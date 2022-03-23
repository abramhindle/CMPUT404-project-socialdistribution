import base64
from cmath import e
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from api.serializers import AuthorSerializer, FollowersSerializer, PostSerializer
from api.util import page_number_pagination_class_factory
from posts.models import Post, ContentType
from follow.models import Follow


class AuthorViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    pagination_class = page_number_pagination_class_factory([('type', 'authors')])

    queryset = get_user_model().objects.filter(is_active=True, is_staff=False, is_api_user=False).order_by('id')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']


class PostViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    pagination_class = page_number_pagination_class_factory([('type', 'posts')])

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs['author_pk']).order_by('-date_published')

    # detail indicates  whether we can do this on the list (false), or only a single item (true)
    @action(methods=['get'], detail=True, url_path='image', name='image')
    def image(self, request, **kwargs):
        author_id = kwargs['author_pk']
        post_id = kwargs['pk']

        img = get_object_or_404(Post.objects, author_id=author_id, pk=post_id)

        if img.content_type != ContentType.PNG and img.content_type != ContentType.JPG:
            return Response(status=404)

        with open(os.path.abspath(settings.BASE_DIR) + img.img_content.url, 'rb') as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode('utf-8')

        return HttpResponse(encoded_img, content_type=img.content_type)


class FollowersViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    pagination_class = page_number_pagination_class_factory([('type', 'followers')])
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        return Follow.objects.filter(followee=self.kwargs['author_pk']).order_by('-created')

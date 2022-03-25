import base64
import requests
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from socialdistribution.storage import ImageStorage
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

        post = get_object_or_404(Post.objects, author_id=author_id, pk=post_id)

        if post.content_type != ContentType.PNG and post.content_type != ContentType.JPG:
            return Response(status=404)

        location = post.img_content.url if post.img_content else post.content
        encoded_img = base64.b64encode(requests.get(location).content)

        return HttpResponse(encoded_img, content_type=post.content_type)


class FollowersViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    pagination_class = page_number_pagination_class_factory([('type', 'followers')])
    serializer_class = FollowersSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']

    def get_queryset(self):
        return Follow.objects.filter(followee=self.kwargs['author_pk']).order_by('-created')

    def update(self, request, *args, **kwargs):
        followee_id = kwargs['author_pk']
        follower_id = kwargs['pk']
        try:
            followee = get_user_model().objects.get(id=followee_id)
            follower = get_user_model().objects.get(id=follower_id)
        except get_user_model().DoesNotExist as e:
            raise Http404

        follow, create = Follow.objects.get_or_create(followee=followee, follower=follower)
        if not create:
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            return Response(status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        followee_id = kwargs['author_pk']
        follower_id = kwargs['pk']
        try:
            followee = get_user_model().objects.get(id=followee_id)
            follower = get_user_model().objects.get(id=follower_id)
        except get_user_model().DoesNotExist as e:
            raise Http404
        Follow.objects.unfollow(followee=followee, follower=follower)
        return Response(status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        followee_id = kwargs['author_pk']
        follower_id = kwargs['pk']
        try:
            followee = get_user_model().objects.get(id=followee_id)
            follower = get_user_model().objects.get(id=follower_id)
        except get_user_model().DoesNotExist as e:
            raise Http404

        follow = get_object_or_404(Follow.objects, follower=follower, followee=followee)
        serializer = self.serializer_class(follow, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

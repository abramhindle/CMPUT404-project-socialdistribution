from backend.apis.friendapi import FriendAPI
from rest_framework import routers
#from .api import AuthorViewSet, CommentViewSet, LikeAPI, NameAPI, RegisterAPI, PostViewSet, LoginAPI, LikedAPI, InboxAPI, FollowerAPI
from .apis import *
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [
    # Register
    path('api/auth/register', RegisterAPI.as_view(), name='author_register'),

    # Author
    path('author/<str:id>/', AuthorViewSet.as_view(
        {'post': 'update', 'get': 'retrieve'}), name='author_update'),
    path('api/authors',
         AuthorViewSet.as_view({'get': 'list'}), name='author_list'),

    # Login
    path('api/auth/login',
         LoginAPI.as_view({'post': 'update'}), name='author_login'),

    # Posts
    path('author/<str:author_id>/posts/',
         PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts_create'),
    path('author/<str:author_id>/posts/<str:id>/', PostViewSet.as_view(
        {'get': 'retrieve', 'post': 'update', 'delete': 'destroy', 'put': 'create'}), name='posts_update'),

    # Comments
    path('author/<str:author_id>/posts/<str:post_id>/comments',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments_create'),

    # Likes
    path('author/<str:author_id>/post/<str:post_id>/likes',
         LikeAPI.as_view({'get': 'list'}), name='like_post'),
    path('author/<str:author_id>/post/<str:post_id>/comments/<str:comment_id>/likes',
         LikeAPI.as_view({'get': 'list'}), name='like_comment'),
    path('author/<str:author_id>/liked',
         LikedAPI.as_view({'get': 'list'}), name='like_confirm'),

    # Querying
    path('api/query/displayName',
         NameAPI.as_view({'post': 'list'}), name='get_name'),

    # Inbox
    path('author/<str:author_id>/inbox',
         InboxAPI.as_view({'get': 'list', 'post': 'create'}), name='get_inbox'),

    # Followers
    path('author/<str:author_id>/followers',
         FollowerAPI.as_view({'get': 'list'}), name='get_follower_list'),
    path('author/<str:author_id>/followers/<str:foreign_id>',
         FollowerAPI.as_view({'delete': 'destroy', 'put': 'create', 'get': 'retrieve'}), name='update_followers'),

    # Friends
    path('author/<str:author_id>/friends',
         FriendAPI.as_view({'get': 'list'}), name='friends_api'),
]

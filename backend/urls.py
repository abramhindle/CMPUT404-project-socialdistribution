from backend.apis.friendapi import FriendAPI
from rest_framework import routers
from .apis import *
from django.urls import path, include
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('author', AuthorViewSet, 'authors')

urlpatterns = [
    # Register
    path('api/auth/register',
         RegisterAPI.as_view(), name='author_register'),

    # Login
    path('api/auth/login',
         LoginAPI.as_view({'post': 'update'}), name='author_login'),

    # Author
    path('author/<str:id>/',
         AuthorViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='author_object'),
    path('authors',
         AuthorViewSet.as_view({'get': 'list'}), name='author_list'),

    # Posts
    path('author/<str:author_id>/posts/',
         PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts_object'),
    path('author/<str:author_id>/posts/<str:id>',
         PostViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'destroy', 'put': 'create'}), name='post_object'),

    # Comments
    path('author/<str:author_id>/posts/<str:post_id>/comments',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments_object'),

    # Likes
    path('author/<str:author_id>/post/<str:post_id>/likes',
         LikeAPI.as_view({'get': 'list'}), name='like_post'),
    path('author/<str:author_id>/post/<str:post_id>/comments/<str:comment_id>/likes',
         LikeAPI.as_view({'get': 'list'}), name='like_comment'),

    # Liked
    path('author/<str:author_id>/liked',
         LikedAPI.as_view({'get': 'list'}), name='liked_list'),

    # Querying
    path('api/query/displayName',
         NameAPI.as_view({'post': 'list'}), name='display_names'),

    # Inbox
    path('author/<str:author_id>/inbox',
         InboxAPI.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='inbox_object'),

    # Followers
    path('author/<str:author_id>/followers',
         FollowerAPI.as_view({'get': 'list'}), name='followers_list'),
    path('author/<str:author_id>/followers/<str:foreign_id>',
         FollowerAPI.as_view({'delete': 'destroy', 'put': 'create', 'get': 'retrieve'}), name='update_followers'),

    # Friends
    path('author/<str:author_id>/friends',
         FriendAPI.as_view({'get': 'list'}), name='friends_api'),
]

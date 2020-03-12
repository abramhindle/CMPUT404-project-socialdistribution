from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),

    url(r'^auth/register/$', CreateAuthorAPIView.as_view(), name='auth_user_create'),
    url(r'^auth/logout/$', AuthorLogoutAPIView.as_view(), name='auth_user_logout'),
    url(r'^auth/getuser/$', GetAuthorAPIView.as_view(), name='auth_user_get'),
    path('auth/edituser/<uuid:pk>',
         AuthorUpdateAPIView.as_view(), name='auth_user_update'),
    url(r'^auth/createpost/$', CreatePostAPIView.as_view(), name='auth_post_create'),
    url(r'^auth/getpost/$', GetPostAPIView.as_view(), name='auth_post_get'),
    url(r'^auth/deletepost/$', DeletePostAPIView.as_view(), name='auth_post_delete'),
    url(r'^auth/getallpost/$', GetAllAuthorPostAPIView.as_view(),
        name='auth_post_getall'),


    # Updated paths

    # Get post
    path('posts/<uuid:pk>', GetPostAPIView.as_view(), name='get_post'),

    # Get post comments
    path('posts/<uuid:pk>/comments',
         GetPostCommentsAPIView.as_view(), name='get_post_comments'),

    # Create post
    path('author/<uuid:pk>/post', CreatePostAPIView.as_view(), name='create_post'),

    # Create friend request
    path('friendrequest/', CreateFriendRequestAPIView.as_view(),
         name='create_friend_request/'),

    # Get all friend requests by author
    path('author/<uuid:pk>/friendrequest',
         GetAllAuthorFriendRequest.as_view(), name='all_author_friend_request'),

    # Get all posts by author
    path('author/<uuid:pk>/posts/', GetAllAuthorPostAPIView.as_view(),
         name='all_author_posts'),

    # Get all public posts
    path('author/posts/',
         GetAllVisiblePostAPIView.as_view(), name='get_all_posts'),

    # Get author object
    path('author/<uuid:pk>', GetAuthorAPIView.as_view(), name='get_author'),

    # Create comment
    path('posts/<uuid:pk>/comment/',
         CreateCommentAPIView.as_view(), name='create_comment'),



    # url(r'^author/<uuid:pk>/friends/<uuid:pk2>',
    #     GetAllAuthorFriends.as_view(), name='get_all_author_friends'),
    # url(r'^author/<uuid:pk>/friends/<uuid:pk>',
    #     GetAllAuthorFriends.as_view(), name='get_all_author_friends'),





    path('login', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),

    path('newpost', new_post, name='new_post'),
    path('requests', requests, name='requests'),
    # path('author/posts', views.feed, name='private_feed'),
    path('posts', explore, name='explore'),

    path('feed', feed, name="my_feed"),

    # path('author/<uuid:author_id>/posts', views.author, name='author_page'),
    path('posts/<uuid:post_id>', post, name='post'),
    path('posts/<uuid:post_id>/comments',
         post_comment, name='post_comment'),
    path('author/<uuid:author_id>/friends', friends, name='friends'),

    # """Optional Pages"""
    path('search', search, name='search'),
    path('account', account, name='account'),
]

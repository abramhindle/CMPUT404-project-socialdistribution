from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url
from .views import *
from .api_views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

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
    path('posts',
         GetAllPublicPostsAPIView.as_view(), name='get_all_posts'),

    # Get all posts visible to user
    path('author/posts', GetAllVisiblePostsAPIView.as_view(),
         name='get_visible_posts'),

    # Get author object
    path('author/<uuid:pk>', GetAuthorAPIView.as_view(), name='get_author'),

    # Create comment
    path('posts/<uuid:pk>/comment/',
         CreateCommentAPIView.as_view(), name='create_comment'),

    # Get all author's friends
    path('author/<uuid:pk>/friends',
         GetAllAuthorFriendsAPIView.as_view(), name='all_author_friends'),

    # Get all author's foaf (includes friends)
    path('friend/<uuid:pk>/foaf',
         GetAllFOAFAPIView.as_view(), name='get_author_foaf'),

    # Get all authors
    path('author/all/', GetAllAuthorsAPIView.as_view(), name='all_authors'),

    # Create friend (pk of friend request)
    path('friend/<uuid:pk>', CreateFriendAPIView.as_view(), name='create_friend'),

    # Delete friend (pk of friend)
    path('friend/<uuid:pk>/delete',
         DeleteFriendAPIView.as_view(), name='delete_friend'),

    # url(r'^author/<uuid:pk>/friends/<uuid:pk2>',
    #     GetAllAuthorFriends.as_view(), name='get_all_author_friends'),
    # url(r'^author/<uuid:pk>/friends/<uuid:pk>',
    #     GetAllAuthorFriends.as_view(), name='get_all_author_friends'),s

    path('', explore, name='explore'),
    path('login', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),

    path('newpost', new_post, name='new_post'),
    path('edit/<uuid:pk>', edit_post, name='edit_post'),
    # path('requests', requests, name='requests'),
    #     path('explore', explore, name='explore'),

    path('feed', feed, name="my_feed"),

    path('notifications', notifications, name='notifications'),
    path('friendrequest', friendrequest, name='friend_request'),
    path('delete/<uuid:post_id>', delete_post, name='delete_post'),
    path('edit_post/<uuid:post_id>', edit_post, name='edit_post'),
    path('media/<str:url>', get_image, name='get_image'),

    # """Optional Pages"""
    path('search', search, name='search'),
    path('account', account, name='account'),
]

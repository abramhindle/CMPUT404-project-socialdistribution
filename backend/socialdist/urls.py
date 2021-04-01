"""socialdist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from rest_framework import routers
from presentation.Viewsets import *
from presentation import views
from rest_framework_jwt.views import obtain_jwt_token as obtainJwtToken
from .views import index

# just some url pattern from requirement, need to implement all of them
urlpatterns = [
    path('author/', AuthorViewSet.as_view({'post': 'create'})),
    path('author/<str:author_id>/',
         AuthorViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('author/<str:author_id>/followers/',
         FollowerViewSet.as_view({'get': 'list'})),
    path('author/<str:author_id>/followers/<str:foreign_author_id>/',
         FollowerViewSet.as_view({'get': 'retrieve'})),
    path('author/<str:author_id>/posts/',
         PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:post_id>/',
         PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'post': 'build'})),
    path('author/<str:author_id>/posts/<str:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/',
         CommentViewSet.as_view({'get': 'retrieve'})),
    path('author/<str:author_id>/inbox/',
         LikesViewSet.as_view({'post': 'create'})),
    path('author/<str:author_id>/inbox/box/',
         InboxViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'delete'})),
    path('author/<str:author_id>/liked/',
         LikedViewSet.as_view({'get': 'list'})),
    path('author/<str:author_id>/posts/<str:post_id>/likes/',
         LikesViewSet.as_view({'get': 'list','post':'create'})),
    path('author/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/',
         LikesViewSet.as_view({'get': 'list'})),
    path('friend-request/', RequestViewSet.as_view({'post': 'create'})),
    path('author/<str:object_id>/request/<str:actor_id>/',
         RequestViewSet.as_view({'delete': 'delete'})),
    path('current-user/', views.currentUser),
    path('user-author/', views.getAuthorForUser),
    path('post-list/', views.getAllPublicPosts),
    path('usermod/<str:username>/', views.getUserMod),
    #     path('users/', views.UserList.as_view()),
    path('token-auth/', obtainJwtToken),
    path('author/<str:author_id>/friends-list/', views.getFriendsList),
    path('author/<str:author_id>/inbox-post/', views.getInboxPost),
    path('author/<str:author_id>/inbox-request/', views.getInboxRequest),
    path('author/<str:author_id>/inbox-like/', views.getInboxLike),
    path('all-authors/', views.getAllAuthors),
    url(r'^.*/', index), # path('', index),
    path('admin/', admin.site.urls),
]

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
from rest_framework import routers
from presentation.Viewsets import *
from presentation import views
from rest_framework_jwt.views import obtain_jwt_token

# register the viewset with a router, and allow the urlconf to be automatically generated
router = routers.DefaultRouter()
router.register(r'author', AuthorViewSet, 'author')


# just some url pattern from requirement, need to implement all of them
urlpatterns = [
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
         LikesViewSet.as_view({'get': 'list'})),
    path('author/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/',
         LikesViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
    path('friend-request/', RequestViewSet.as_view({'post': 'create'})),
    path('current-user/', views.current_user),
    path('user-author/', views.get_author_for_user),
    path('post-list/', views.get_all_public_posts),
    path('users/', views.UserList.as_view()),
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_jwt_token),
    path('author/<str:author_id>/friends-list/', views.get_friends_list),
    path('author/<str:author_id>/inbox-post/', views.get_inbox_post),
    path('author/<str:author_id>/inbox-request/', views.get_inbox_request),
    path('author/<str:author_id>/inbox-like/', views.get_inbox_like)
]

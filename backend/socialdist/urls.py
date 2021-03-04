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

# register the viewset with a router, and allow the urlconf to be automatically generated
router = routers.DefaultRouter()
router.register(r'author', AuthorViewSet, 'author')


# just some url pattern from requirement, need to implement all of them
urlpatterns = [
    path('author/<str:author_id>/followers',
         FollowerViewSet.as_view({'get': 'list'})),
    path('author/<str:author_id>/followers/<str:foreign_author_id>/',
         FollowerViewSet.as_view({'get': 'retrieve'})),
    path('author/<str:author_id>/posts/',
         PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:post_id>',
         PostViewSet.as_view({'get': 'retrieve', 'post': 'update', 'put': 'build'})),
    path('author/<str:author_id>/posts/<str:post_id>/comments',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('author/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>',
         CommentViewSet.as_view({'get': 'retrieve'})),
    path('author/<str:author_id>/inbox',
         InboxViewSet.as_view({'get': 'retrieve', 'post': 'update', 'delete': 'delete'})),
    path('', include(router.urls)),
    path('current_user/', views.current_user),
    path('users/', views.UserList.as_view()),
    path('admin/', admin.site.urls),
]

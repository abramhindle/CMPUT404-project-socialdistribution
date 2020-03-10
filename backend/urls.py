"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from backend.apiviews.post_views import PostViewSet
from backend.apiviews.author_views import AuthorViewSet
from backend.apiviews.friend_request_views import FriendRequestViewSet
from backend.apiviews.friend_views import FriendViewSet

from .views import index
router = DefaultRouter()

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),

    # url for Post Operations
    path('posts/', PostViewSet.as_view({
        "get": "list"
    })),
    path('posts/<uuid:postId>/', PostViewSet.as_view({
        "get": "retrieve",
        "delete": "destroy",
        "put": "partial_update",
    })),
    path('posts/<uuid:postId>/', PostViewSet.as_view({
        "get": "retrieve"
    })),
    path('author/posts', PostViewSet.as_view({
        "get": "get_user_visible_posts",
        "post": "create_post"
    })),
    path('author/<path:author_id>/posts', PostViewSet.as_view({
         "get": "visible_posts"
         })),

    # url of Author Operations
    path('author/', AuthorViewSet.as_view({
        "get": "get_authors"
    })),
    path('author/<path:pk>/', AuthorViewSet.as_view({
        "get": "get_profile"
    })),
    path('author/<path:pk>/friends', AuthorViewSet.as_view(({
        "get": "get_friends"
    }))),
    path('friendrequest/', FriendRequestViewSet.as_view(), name='friendrequest'),
    # path("friendrequest/all", FriendRequestViewSet.as_view({"get": "list"}))
    path('friend/accept', FriendViewSet.as_view(), name="friend"),

]

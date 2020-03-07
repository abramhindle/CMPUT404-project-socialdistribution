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

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    # Url for Post Operations
    path('posts/', PostViewSet.as_view({"get": "list"})),
    path('posts/<uuid:postId>/', PostViewSet.as_view({
        "get": "retrieve",
        "delete": "destroy",
        "put": "partial_update",
        })),
    path('posts/<uuid:postId>/', PostViewSet.as_view({"get": "retrieve"})),
    path('author/posts', PostViewSet.as_view({
        "get":"get_user_visible_posts",
        "post":"create_post"
        })) 
]
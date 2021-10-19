"""Social_Distribution URL Configuration

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
from django.urls import path, include
from . import views

urlpatterns = [
    # /authors/login
    path('login', views.login.as_view(), name='login'),
    # /authors/logout
    path('logout', views.logout.as_view(), name='logout'),
    # /authors/register
    path('register', views.register.as_view(), name='register'),
    # /authors/
    path('', views.index.as_view(), name='index'),
    # /authors/{author_id}
    path('<str:author_id>', views.profile.as_view(), name='profile'),
    # /authors/{author_id}/followers
    path('<str:author_id>/followers', views.followers.as_view(), name='followers'),
    # /authors/{author_id}/followers
    path('<str:author_id>/followers/<str:foreign_author_id>', views.follower.as_view(), name='follower'),
    # /authors/{author_id}/liked
    path('<str:author_id>/liked', views.liked.as_view(), name='liked'),
    # /authors/{author_id}/inbox
    path('<str:author_id>/inbox', views.inbox.as_view(), name='inbox'),
]

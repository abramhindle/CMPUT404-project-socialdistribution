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
    # /author/login
    path('author/login', views.login.as_view(), name='login'),
    # /author/logout
    path('author/logout', views.logout.as_view(), name='logout'),
    # /author/register
    path('author/register', views.register.as_view(), name='register'),
    # /authors/
    path('authors', views.index.as_view(), name='index'),
    path('authors/all', views.allAuthors.as_view(), name='allAuthors'),
    # /author/{author_id}
    path('author/<str:author_id>', views.profile.as_view(), name='profile'),
    # /author/{author_id}/followers
    path('author/<str:author_id>/followers', views.followers.as_view(), name='followers'),
    # /author/{author_id}/followers/{foreign_author_id}
    path('author/<str:author_id>/followers/<str:foreign_author_id>', views.follower.as_view(), name='follower'),
    # /author/{author_id}/liked
    path('author/<str:author_id>/liked', views.liked.as_view(), name='liked'),
    # /author/{author_id}/inbox
    path('author/<str:author_id>/inbox', views.inbox.as_view(), name='inbox'),

    # /author/login
    path('author/login/', views.login.as_view(), name='login'),
    # /author/logout
    path('author/logout/', views.logout.as_view(), name='logout'),
    # /author/register
    path('author/register/', views.register.as_view(), name='register'),
    # /authors/
    path('authors/', views.index.as_view(), name='index'),
    path('authors/all/', views.allAuthors.as_view(), name='allAuthors'),
    # /author/{author_id}
    path('author/<str:author_id>/', views.profile.as_view(), name='profile'),
    # /author/{author_id}/followers
    path('author/<str:author_id>/followers/', views.followers.as_view(), name='followers'),
    # /author/{author_id}/followers/{foreign_author_id}
    path('author/<str:author_id>/followers/<str:foreign_author_id>/', views.follower.as_view(), name='follower'),
    path('author/<str:author_id>/followers/<path:foreign_author_id>/', views.follower.as_view(), name='follower'),
    # /author/{author_id}/liked
    path('author/<str:author_id>/liked/', views.liked.as_view(), name='liked'),
    # /author/{author_id}/inbox
    path('author/<str:author_id>/inbox/', views.inbox.as_view(), name='inbox'),
]

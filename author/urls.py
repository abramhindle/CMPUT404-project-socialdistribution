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
    # /author/
    path('', views.index, name='index'),
    # /author/{author_id}
    path('<str:author_id>', views.profile, name='profile'),
    # /author/{author_id}/followers
    path('<str:author_id>/followers', views.followers.as_view(), name='followers'),
    # /author/{author_id}/followers
    path('<str:author_id>/followers/<int:foreign_author_id>', views.follower, name='follower'),
    # /author/{author_id}/liked
    path('<str:author_id>/liked', views.liked, name='liked'),
    # /author/{author_id}/inbox
    path('<str:author_id>/inbox', views.inbox, name='inbox'),
]

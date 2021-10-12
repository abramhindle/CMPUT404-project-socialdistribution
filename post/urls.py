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
from . import views
from django.urls import path, include

urlpatterns = [
    # /author/{author_id}/post/
    path('', views.index, name='posts'),
    # /author/{author_id}/post/{post_id}
    path('<str:post_id>', views.post, name='post'),
    # /author/{author_id}/post/{post_id}/comments
    path('<str:post_id>/comments', views.comments, name='comments'),
    # /author/{author_id}/post/{post_id}/likes
    path('<str:post_id>/likes', views.likes, name='likes'),
    # /author/{author_id}/post/{post_id}/comments/{comment_id}/likes
    path('<str:post_id>/comments/<int:comment_id>/likes', views.commentLikes, name='likes'),
]

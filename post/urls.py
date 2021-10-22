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
    # /author/{author_id}/posts/
    path('posts/', views.index.as_view(), name='posts'),
    # /author/{author_id}/posts/{post_id}
    path('posts/<str:post_id>', views.post.as_view(), name='post'),
    # /author/{author_id}/posts/{post_id}/comments
    path('posts/<str:post_id>/comments', views.comments.as_view(), name='comments'),
    # /author/{author_id}/post/{post_id}/likes
    path('post/<str:post_id>/likes', views.likes.as_view(), name='likes'),
    # /author/{author_id}/post/{post_id}/comments/{comment_id}/likes
    path('post/<str:post_id>/comments/<str:comment_id>/likes', views.commentLikes.as_view(), name='likes'),
]

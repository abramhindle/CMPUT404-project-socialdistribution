from django.urls import path, include

from authors import views
from .views import *
from posts.views import PostDetail, PostList, CommentDetail

urlpatterns = [
    path('<str:author_id>/', AuthorDetail.as_view(), name="author-detail"),
    path('<str:author_id>/posts/<str:post_id>/', PostDetail.as_view(), name="post-detail"),
    path('<str:author_id>/posts/', PostList.as_view(), name="post-list"),
    path('<str:author_id>/posts/<str:post_id>/comments', CommentDetail.as_view(), name="comment-detail")
]

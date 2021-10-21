from django.urls import path, include, re_path

from authors import views
from .views import *
from posts.views import PostDetail, PostList, CommentList

urlpatterns = [
    # server to server API
    path('<str:author_id>/posts/<str:post_id>/',
         PostDetail.as_view(), name="post-detail"),
    path('<str:author_id>/inbox/', InboxListView.as_view(), name="author-inbox"),
    path('<str:author_id>/', AuthorDetail.as_view(), name="author-detail"),
    path('<str:author_id>/posts/<str:post_id>/', PostDetail.as_view(), name="post-detail"),
    path('<str:author_id>/posts/', PostList.as_view(), name="post-list"),
    path('<str:author_id>/posts/<str:post_id>/comments/', CommentList.as_view(), name="comment-list"),

    path('<str:author_id>/followers/', FollowerList.as_view(), name="author-followers"),
    re_path(r'^(?P<author_id>[^/]*)/followers/(?P<foreign_author_url>.*)$', FollowerDetail.as_view(), name="author-follower-detail"),

    # extra internal API for client
    re_path(r'^(?P<author_id>[^/]*)/friend-request/(?P<foreign_author_url>.*)$',
            internally_send_friend_request, name="friend-request"),
]

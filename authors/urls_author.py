from django.urls import path, include, re_path

from authors import views
from .views import *
from posts.views import PostDetail

urlpatterns = [
    # server to server API
    path('<str:author_id>/posts/<str:post_id>/',
         PostDetail.as_view(), name="post-detail"),
    path('<str:author_id>/inbox/', InboxListView.as_view(), name="author-inbox"),
    path('<str:author_id>/', AuthorDetail.as_view(), name="author-detail"),

    # extra internal API for client

    re_path(r'^(?P<author_id>[^/]*)/friend-request/(?P<foreign_author_url>.*)$',
            internally_send_friend_request, name="friend-request"),
]

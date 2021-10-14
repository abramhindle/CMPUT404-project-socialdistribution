from django.urls import path, include, re_path

from authors import views
from .views import *
from posts.views import PostDetail

urlpatterns = [
    # server to server API
    path('<str:author_id>/posts/<str:post_id>/', PostDetail.as_view(), name="post-detail"),
    path('<str:author_id>/inbox/', inbox, name="author-inbox"),
    path('<str:author_id>/', AuthorDetail.as_view(), name="author-detail"),

    # extra internal API for client
    
    # author_id: anything other than slash
    # foreign_author_url: anything
    re_path(r'^(?P<author_id>[^/]*)/friend-request/(?P<foreign_author_url>.*)$', internally_send_friend_request, name="friend-request"),
]

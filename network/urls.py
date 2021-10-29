from django.conf.urls import url
from django.urls import path, include
from backend.views import *
from network.views import *

urlpatterns = [
    path('', apiOverview, name="apiOverview"),
    path('authors/', AuthorList, name ='authorList'),
    path('author/<str:author_uuid>/', AuthorDetail, name="authorDetail"),
    path('author/<str:author_uuid>/followers/', FollowerList, name="followerList"),
    path('author/<str:author_uuid>/followers/<str:follower_uuid>/', FollowerDetail, name="followerDetail"),
    path('author/<str:author_uuid>/posts/', PostList, name="postList"),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/', PostDetail, name="postDetail"),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/comments/', CommentList, name="commentList"),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/comments/<str:comment_uuid>/', CommentDetail, name="commentDetail"),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/likes/', LikeList, name="likeListPost"),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/comments/<str:comment_uuid>/likes/', LikeList, name="likeListComment"),
    path ('accounts/', UserPost, name='account-create'),
    path('auth/', include('rest_auth.urls'), name='auth'),    
    path('auth/register/', include('rest_auth.registration.urls'), name='auth-register'),
    path('auth/login/', include('rest_auth.registration.urls'), name='auth-login'),
    path('auth/register/', null_view, name='account_inactive')
]

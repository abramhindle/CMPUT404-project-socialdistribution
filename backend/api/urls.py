from django.urls import path, re_path, include
from django.conf.urls import url

from .views import index, authorView, followerView, postView, authView, likeView, likedView, commentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Index
    path('', index.index, name="index"),
    
    # Auth Endpoints
    path('author/login/', authView.LoginView.as_view(), name="login"),
    path('author/register/', authView.SignupView, name="register"),

    # Author Endpoints
    path('authors/',authorView.AuthorList, name ='authorList'),
    path('author/<str:author_uuid>/', authorView.AuthorDetail, name="authorDetail"),

    # Follower Endpoints
    path('author/<str:author_uuid>/followers/', followerView.FollowerList, name="followerList"),
    path('author/<str:author_uuid>/followers/<str:follower_uuid>/', followerView.FollowerDetail, name="followerDetail"),

    # Post Endpoints
    # path('author/<str:authorID>/stream/', postView.getStreamPosts, name="streamPosts"),
    path('author/<str:author_uuid>/posts/', postView.PostList, name="authorPosts"),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/', postView.PostDetail, name="authorPost"),

    # Comment Endpoints
    path('author/<str:author_uuid>/posts/<str:post_uuid>/comments/', commentView.CommentList, name='commentList'),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/comments/<str:comment_uuid>/', commentView.CommentDetail, name='commentDetail'),

    # Liked Endpoints
    path('author/<str:author_uuid>/liked/', likedView.LikedList, name="likedList"),

    # Like Endpoints
    path('author/<str:author_uuid>/posts/<str:post_uuid>/likes/', likeView.LikeListPost, name="likeListPost"),
    path('author/<str:author_uuid>/posts/<str:post_uuid>/comments/<str:comment_uuid>/likes/', likeView.LikeListComment, name="likeListComment"),

    # Token Endpoints
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]


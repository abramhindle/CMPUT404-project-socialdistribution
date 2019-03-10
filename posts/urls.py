from django.urls import path
from .views import AdminUserView
from . import views
from .views import UserView, PostView, PostViewID, CommentViewList

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<pk>', PostViewID.as_view(), name='postid'),
    path('posts/<post_id>/comments/', CommentViewList.as_view(), name='comments'),
    path('users/', UserView.as_view(), name='users'),
    path('users/approve/', AdminUserView.as_view(), name='admin-users'),
]

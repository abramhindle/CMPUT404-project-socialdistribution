from django.urls import path
from .views import UserView, PostView, PostViewID, FrontEndPostViewID, CommentViewList

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('posts/', PostView.as_view(), name='posts'),
    path('frontend/posts/<pk>', FrontEndPostViewID.as_view(), name='frontpostid'),
    path('posts/<pk>', PostViewID.as_view(), name='postid'),
    path('posts/<post_id>/comments/', CommentViewList.as_view(), name='comments')
]

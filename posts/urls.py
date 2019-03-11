from django.urls import path
from .views import UserView, PostView, PostViewID, CommentViewList,FriendRequestView,FriendListView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('author/<pk>/friends', FriendListView.as_view(), name='friendslist'),
    #path('author/<authorid1>/friends/<service2>/author/<authorid2>', AreFriendsView.as_view(), name='arefriends'),
    #path('author/<authorid1>/friends/<authorid2>', AreFriendsView.as_view(), name='arefriends'),
    path('friendrequest/', FriendRequestView.as_view(), name='friendrequest'),
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<pk>', PostViewID.as_view(), name='postid'),
    path('posts/<post_id>/comments/', CommentViewList.as_view(), name='comments')
]

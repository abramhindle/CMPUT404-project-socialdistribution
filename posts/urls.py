from django.urls import path
from .views import UserView,FriendListView,AreFriendsView, FriendReqView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('author/<pk>/friends', FriendListView.as_view(), name='friends'),
    path('author/<authorid1>/friends/<service2>/author/<authorid2>', AreFriendsView.as_view(), name='arefriends'),
    path('friendrequest/', FriendReqView.as_view(), name='friendreq')
]
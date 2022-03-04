from django.urls import path
from .views import (
    FriendRequestsView,
    MyFriendsView,
    create_follow_request,
    accept_follow_request,
    unfollow_request,
    reject_follow_request,
    UsersView
)

app_name = 'follow'
urlpatterns = [
    path('users/<slug:to_username>/request/', view=create_follow_request, name='create_follow_request'),
    path('users/<slug:from_username>/accept/', view=accept_follow_request, name='accept_follow_request'),
    path('users/<slug:from_username>/reject/', view=reject_follow_request, name='reject_follow_request'),
    path('users/<slug:from_username>/unfollow/', view=unfollow_request, name='unfollow_request'),
    path('friend-requests', view=FriendRequestsView.as_view(), name='friend_requests'),
    path('friends', view=MyFriendsView.as_view(), name='friends'),
    path('', view=UsersView.as_view(), name='users'),
]

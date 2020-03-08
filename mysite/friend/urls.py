from rest_framework import routers
from django.urls import path, include
from .views import FriendViewSet,FriendRequestViewSet,IfFriendViewSet

router = routers.SimpleRouter()

router.register("my_friends", FriendViewSet, basename="friend")
router.register("friend_request", FriendRequestViewSet, basename="friend")
router.register("if_friend", IfFriendViewSet, basename="friend")

urlpatterns = [
    path("",include(router.urls))
]
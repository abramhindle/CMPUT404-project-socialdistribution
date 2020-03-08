from rest_framework import routers
from django.urls import path, include
from .views import FriendViewSet,FriendRequestViewSet

router = routers.SimpleRouter()

router.register("my_friends", FriendViewSet, basename="friend")
router.register("friend_request", FriendRequestViewSet, basename="friend")

urlpatterns = [
    path("",include(router.urls))
]
from rest_framework import routers
from django.urls import path, include
from .views import FriendViewSet,FriendRequestViewSet

router = routers.SimpleRouter()

router.register("myFriends", FriendViewSet, basename="friend")
router.register("friendRequest", FriendRequestViewSet, basename="friend")

urlpatterns = [
    path("",include(router.urls))
]
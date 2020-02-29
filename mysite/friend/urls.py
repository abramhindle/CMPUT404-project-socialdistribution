from rest_framework import routers
from django.urls import path, include
from .views import FriendViewSet

router = routers.DefaultRouter()
router.register("friendRequest", FriendViewSet, basename="friend")


urlpatterns = [
    path("", include(router.urls)),
]

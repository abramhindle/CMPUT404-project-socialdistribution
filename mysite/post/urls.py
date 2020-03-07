from rest_framework import routers
from django.urls import path, include

from .views import UserPostsViewSet, VisiblePostsViewSet

router = routers.DefaultRouter()
router.register("UserPosts", UserPostsViewSet, basename="post")
router.register("visiblePosts", VisiblePostsViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]

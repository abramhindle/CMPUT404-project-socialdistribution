from rest_framework import routers
from django.urls import path, include

from .views import MyPostViewSet, VisiblePostViewSet

router = routers.DefaultRouter()
router.register("myPosts", MyPostViewSet, basename="post")
router.register("visiblePosts", VisiblePostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]

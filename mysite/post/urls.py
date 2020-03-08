from rest_framework import routers
from django.urls import path, include

from .views import PostsViewSet

router = routers.DefaultRouter()
router.register("", PostsViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]

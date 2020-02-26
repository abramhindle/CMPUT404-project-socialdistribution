from rest_framework import routers
from django.urls import path, include

from .views import PostViewSet

router = routers.DefaultRouter()
router.register("", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

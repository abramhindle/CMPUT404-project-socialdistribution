from rest_framework import routers
from django.urls import path, include
from .views import NodeViewSet

router = routers.DefaultRouter()

router.register("nodes",NodeViewSet,basename="node")

urlpatterns = [
    path("",include(router.urls))
]

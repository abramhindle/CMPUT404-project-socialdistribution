from django.conf.urls import include, url
from rest_framework import routers

from .api import DummyPostViewSet

router = routers.DefaultRouter()
router.register('dummy_post', DummyPostViewSet)

urlpatterns = [
    url("^", include(router.urls)),
]
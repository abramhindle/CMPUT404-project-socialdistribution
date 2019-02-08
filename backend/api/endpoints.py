from django.conf.urls import include, url
from rest_framework import routers

from .api import DummyPostViewSet
from .view.RegistrationView import RegistrationView

router = routers.DefaultRouter()
router.register('dummy_post', DummyPostViewSet)

urlpatterns = [
    url("^", include(router.urls)),
    url("^auth/register/$", RegistrationView.as_view()),
]
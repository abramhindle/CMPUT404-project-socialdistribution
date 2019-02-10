from django.conf.urls import include, url
from rest_framework import routers

from .api import DummyPostViewSet
from .view.RegistrationView import RegistrationView
from .view.LoginView import LoginView
from .view.AuthorProfileView import AuthorProfileView

router = routers.DefaultRouter()
router.register('dummy_post', DummyPostViewSet)

urlpatterns = [
    url("^", include(router.urls)),
    url("^auth/register/$", RegistrationView.as_view()),
    url("^auth/login/$", LoginView.as_view()),
    url("^profile/$", AuthorProfileView.as_view())
]
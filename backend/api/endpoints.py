from django.conf.urls import include, url
from .view.RegistrationView import RegistrationView
from .view.LoginView import LoginView
from .view.AuthorProfileView import AuthorProfileView
from .view.PostView import PostView

urlpatterns = [
    url("^auth/register/$", RegistrationView.as_view()),
    url("^auth/login/$", LoginView.as_view()),
    url("^profile/$", AuthorProfileView.as_view()),
    url('^post/$', PostView.as_view()),
]
from django.conf.urls import include, url
from .view.RegistrationView import RegistrationView
from .view.LoginView import LoginView
from .view.AuthorProfileView import AuthorProfileView
from .view.CreatePostView import CreatePostView
from .view.CategoryView import CategoryView

urlpatterns = [
    url("^auth/register/$", RegistrationView.as_view()),
    url("^auth/login/$", LoginView.as_view()),
    url(r"^author/(?P<uid>.*)$", AuthorProfileView.as_view()),
    url('^posts/?$', CreatePostView.as_view()),
    url('^categories/$', CategoryView.as_view()),
]
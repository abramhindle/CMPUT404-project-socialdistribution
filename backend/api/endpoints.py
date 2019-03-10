from django.conf.urls import include, url
from .view.RegistrationView import RegistrationView
from .view.LoginView import LoginView
from .view.AuthorProfileView import AuthorProfileView
from .view.CreatePostView import CreatePostView
from .view.CategoryView import CategoryView
from .view.FriendsView import FriendsView
from .view.CheckFriendsView import CheckFriendsView
from .view.CheckFollowersView import CheckFollowersView

urlpatterns = [
    url("^auth/register/$", RegistrationView.as_view()),
    url("^auth/login/$", LoginView.as_view()),
    url(r'^author/(?P<authorid>.*)/friends/?$', CheckFriendsView.as_view()),
    url(r"^author/(?P<uid>.*)$", AuthorProfileView.as_view()),
    url(r'^posts/?(?P<postid>.*)/?$', CreatePostView.as_view()),
    url('^categories/$', CategoryView.as_view()),
    url('^friendrequest/?$', FriendsView.as_view()),
    url('^unfriend/?$', FriendsView.as_view()),
    url(r'^followers/(?P<authorid>.*)$', CheckFollowersView.as_view()),
]
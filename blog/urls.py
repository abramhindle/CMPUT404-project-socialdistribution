# api/urls.py

from django.urls import path
from .views import SignInView, SignOutView


urlpatterns = [
    path("signin/", SignInView.as_view(), name="Sign in"),
    path("signout/", SignOutView.as_view(), name="Sign out"),
]
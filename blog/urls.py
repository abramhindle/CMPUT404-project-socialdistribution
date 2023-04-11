# api/urls.py

from django.urls import path
from .views import SignInView, SignOutView, SignUpView


urlpatterns = [
    path("signin/", SignInView.as_view(), name="Sign in"),
    path("signout/", SignOutView.as_view(), name="Sign out"),
    path("signup/", SignUpView.as_view(), name="Sign up"),
]
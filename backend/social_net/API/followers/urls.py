from django.urls import path
from . import views


urlpatterns = [
  path('authors/<slug:uid>/followers/', views.AuthorFollowersView, name='AuthorFollowersView'),   # FIXME: "/followers" (no slash at end of)
  path('authors/<slug:uid>/followers/<slug:foreign_uid>/', views.AuthorFollowersOperationsView, name='AuthorFollowersOperationsView'),    # FIXME: "/<slug:foreign_uid>" (no slash at end of)
  path('follow/<slug:uid>/<slug:uid2>', views.FollowView, name='FollowView'),
]
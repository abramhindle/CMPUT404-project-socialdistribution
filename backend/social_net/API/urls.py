from django.urls import path
from . import views

urlpatterns = [
  path('authors/<slug:uid>', views.AuthorView, name='AuthorView'),
  path('authors/<slug:uid>/followers/', views.AuthorFollowersView, name='AuthorFollowersView'),
  path('authors/<slug:uid>/followers/<slug:foreign_uid>', views.AuthorFollowersOperationsView, name='AuthorFollowersOperationsView'),
  path('authors', views.AuthorsView, name='AuthorsView'),
  path('follow/<slug:uid>/<slug:uid2>', views.FollowView, name='FollowView'),
]
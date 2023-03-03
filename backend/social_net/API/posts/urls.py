from django.urls import path
from . import views


urlpatterns = [
  path('authors/<slug:author_id>/posts/<slug:post_id>/', views.PostsRetriveView, name='PostsRetriveView'),
  path('authors/<slug:author_id>/posts/', views.PostsView, name='PostsView'),
]
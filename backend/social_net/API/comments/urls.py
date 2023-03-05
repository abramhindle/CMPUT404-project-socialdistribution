from django.urls import path
from . import views


urlpatterns = [
  path('authors/<slug:author_id>/posts/<slug:post_id>/comments', views.CommentsView, name='CommentsView'),
]
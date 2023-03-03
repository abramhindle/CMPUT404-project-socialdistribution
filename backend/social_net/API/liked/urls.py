from django.urls import path
from . import views


urlpatterns = [
  path('authors/<slug:author_id>/liked/', views.LikedView, name='LikedView'),
]
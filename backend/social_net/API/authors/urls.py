from django.urls import path
from . import views

urlpatterns = [
  path('authors/', views.AuthorsView, name='AuthorsView'),
  path('authors/<slug:uid>/', views.AuthorView, name='AuthorView'),
]
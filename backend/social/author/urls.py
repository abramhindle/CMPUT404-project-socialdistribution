from django.urls import path
from . import views
from .views import *


app_name = 'authors'
urlpatterns = [
  path('', views.get_authors, name='get_authors'),
  path('<str:pk_a>/', views.AuthorView.as_view(), name='get_authors'),
  path('authors/<str:pk_a>/followers', views.FollowersView.as_view(), name="get_followers")
]
#path('authors/<str:pk_a>/inbox/', views.LikeView.as_view(), name = "likes"),
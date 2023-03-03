from django.urls import path
from . import views
from .views import PostDeleteView
from .views import ImageView
from .views import *


app_name = 'posts'
urlpatterns = [
  path('authors/<str:pk_a>/posts/', views.post_list.as_view(), name = "posts"),
  path('authors/<str:pk_a>/posts/<str:pk>/', views.post_detail.as_view(), name='detail'),
  path('authors/<str:pk_a>/posts/<str:pk>/comments/', views.get_comments, name='get_comments'),
  path('authors/<str:pk_a>/posts/<str:pk>/likes/', views.get_comments, name='get_likes'),
  path('authors/<str:pk_a>/posts/<str:pk>/image/', ImageView.as_view()),

]

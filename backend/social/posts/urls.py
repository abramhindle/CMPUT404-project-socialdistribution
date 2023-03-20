from django.urls import path
from . import views
from .views import *


app_name = 'posts'
urlpatterns = [
  path('authors/<str:pk_a>/posts/', views.post_list.as_view(), name = "posts"),
  path('authors/<str:pk_a>/posts/<str:pk>/', views.post_detail.as_view(), name='detail'),
  path('authors/<str:pk_a>/posts/<str:pk>/comments/', views.CommentView.as_view(), name='comments'),
  path('authors/<str:pk_a>/posts/<str:pk>/comments/<str:pk_m>', views.CommentDetailView.as_view(), name='comment_detail'),
  path('authors/<str:pk_a>/posts/<str:pk>/likes/', views.get_likes, name='get_likes'),
  path('authors/<str:pk_a>/liked/', views.LikedView.as_view(), name='get_liked'),
  path('authors/<str:pk_a>/posts/<str:pk>/image/', ImageView.as_view()),
  path('authors/<str:origin_author>/posts/<str:post_id>/share/<str:author>', views.ShareView.as_view, name='share'),
]

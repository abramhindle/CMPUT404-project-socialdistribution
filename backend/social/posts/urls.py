from django.urls import path
from . import views
from .views import PostDeleteView
from .views import ImageView


app_name = 'posts'
urlpatterns = [
  path('authors/<str:pk_a>/posts/', views.post_list.as_view(), name = "posts"),
  #path('authors/<str:pk_a>/posts/post/', views.create_posts, name='create_posts'),
  path('authors/<str:pk_a>/posts/<str:pk>/', views.DetailView.as_view(), name='detail'),
  path('authors/<str:pk_a>/posts/<str:pk>/delete/', PostDeleteView.as_view(), name='delete'),
  path('authors/<str:pk_a>/posts/<str:pk>/comments/', views.get_comments, name='get_comments'),
  path('authors/<str:pk_a>/posts/<str:pk>/likes/', views.get_comments, name='get_likes'),
  path('authors/<str:pk_a>/posts/<str:pk>/image/', ImageView.as_view()),

]

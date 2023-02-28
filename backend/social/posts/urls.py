from django.urls import path
from . import views
from .views import PostDeleteView


app_name = 'posts'
urlpatterns = [
    path('authors/posts/', views.get_posts, name='get_posts'),
  path('authors/<str:pk_a>/posts/<str:pk>/', views.DetailView.as_view(), name='detail'),
  path('authors/<str:pk_a>/posts/<str:pk>/delete/', PostDeleteView.as_view(), name='delete')
]

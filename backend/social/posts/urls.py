from django.urls import path
from . import views
from .views import PostDeleteView


app_name = 'posts'
urlpatterns = [
  path('authors/<int:pk_a>/posts/', views.IndexView.as_view(), name='index'),
  path('authors/<int:pk_a>/posts/<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('authors/<int:pk_a>/posts/<int:pk>/delete/', PostDeleteView.as_view(), name='delete')
]

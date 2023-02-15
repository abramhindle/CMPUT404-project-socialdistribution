from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
  path('author<int:pk_a>/', views.IndexView.as_view(), name='index'),
  path('author<int:pk_a>/<int:pk>/', views.DetailView.as_view(), name='detail'),
]
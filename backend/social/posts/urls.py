from django.urls import path
from . import views
from .views import PostDeleteView


app_name = 'posts'
urlpatterns = [
  path('author<int:pk_a>/', views.IndexView.as_view(), name='index'),
  path('author<int:pk_a>/<int:pk>/', views.DetailView.as_view(), name='detail'),
  path('author<int:pk_a>/<int:pk>/delete', PostDeleteView.as_view(), name='delete')
]

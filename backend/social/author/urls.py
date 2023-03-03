from django.urls import path
from . import views
from .views import *


app_name = 'authors'
urlpatterns = [
  path('', views.get_authors, name='get_authors'),
  path('<str:pk_a>/', views.get_authors, name='detail'),
]

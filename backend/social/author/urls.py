from django.urls import path
from . import views
from .views import *


app_name = 'authors'
urlpatterns = [
  path('authors/', views.get_authors, name='get_authors'),
  path('authors/<str:pk_a>/inbox/', views.Inbox_list.as_view(), name = "inbox"),
  path('authors/<str:pk_a>/', views.AuthorView.as_view(), name='get_authors'),
]

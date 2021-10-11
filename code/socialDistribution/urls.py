from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.loginPage, name='login'),
  path('register/', views.register, name='register'),
  path('logout/', views.logoutUser, name='logout'),
  path('home/', views.home, name='home'),
  path('authors/', views.authors, name='authors'),
  path('create/', views.create, name='create'),
  path('post/', views.post, name='post'),
  path('profile/', views.profile, name='profile'),
  path('user/', views.user, name='user'),
]
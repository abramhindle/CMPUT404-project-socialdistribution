from django.urls import path
from . import views

app_name = 'socialDistribution'
urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.loginPage, name='login'),
  path('register/', views.register, name='register'),
  path('logout/', views.logoutUser, name='logout'),
  path('authors/', views.authors, name='authors'),
  path('author/<int:author_id>/', views.author, name='author'),
  path('home/', views.home, name='home'),
  path('author/<int:author_id>/posts/', views.posts, name='posts'),
  path('create/', views.create, name='create'),
  path('profile/', views.profile, name='profile'),
  path('user/', views.user, name='user'),
] 
from django.urls import path
from . import views

app_name = 'socialDistribution'
urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.loginPage, name='login'),
  path('register/', views.register, name='register'),
  path('logout/', views.logoutUser, name='logout'),
  path('author/', views.authors, name='authors'),
  path('author/<int:author_id>/', views.author, name='author'),
  path('home/', views.home, name='home'),
  path('author/<int:author_id>/posts/', views.posts, name='posts'),
  path('author/<int:author_id>/befriend/', views.befriend, name='befriend'),
  path('author/<int:author_id>/un-befriend/', views.un_befriend, name='un-befriend'),
  path('<int:author_id>/accept-friend/', views.accept_friend, name='accept-friend'),
  path('create/', views.create, name='create'),
  path('profile/', views.profile, name='profile'),
  path('user/', views.user, name='user'),
  path('like-post/<int:id>', views.likePost, name='likePost'),
  path('delete-post/<int:id>', views.deletePost, name='deletePost'),
  path('edit-post/<int:id>', views.editPost, name='editPost'),
]

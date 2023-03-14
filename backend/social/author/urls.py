from django.urls import path
from . import views
from .views import *

app_name = 'authors'
urlpatterns = [
  path('', views.get_authors, name='get_authors'),
  path('<str:pk_a>/', views.AuthorView.as_view(), name='detail'),
  path('<str:pk_a>/inbox', views.Inbox_list.as_view(), name='inbox'),
  path('authors/<str:pk_a>/followers/', views.FollowersView.as_view(), name="get_followers"),
  path('authors/<str:pk_a>/followers/<str:pk>', views.FollowersView.as_view(), name="follow"),
  path('<str:pk_a>/sendreq/', views.FriendRequestView.as_view(), name='send_req'),
  path('<str:pk_a>/viewreq/', views.ViewRequests.as_view(), name='get_Requests'),
  path('<str:displayName>', views.getAuthor)
]
#path('authors/<str:pk_a>/inbox/', views.LikeView.as_view(), name = "likes"),
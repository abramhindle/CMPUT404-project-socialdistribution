from django.urls import path
from . import views
from .views import *
import posts.views as pview

app_name = 'authors'
urlpatterns = [
  path('', views.AuthorsListView.as_view(), name='get_authors'),
  path('<str:pk_a>/', views.AuthorView.as_view(), name='detail'),
  path('<str:pk_a>/inbox/', views.Inbox_list.as_view(), name='inbox'),
  path('<str:pk_a>/followers/', views.FollowersView.as_view(), name="get_followers"),
  path('<str:pk_a>/followers/<str:pk>/', views.FollowersView.as_view(), name="follow"),
  path('<str:pk_a>/sendreq/', views.FriendRequestView.as_view(), name='send_req'),
  path('<str:pk_a>/viewreq/', views.ViewRequests.as_view(), name='get_Requests'),
  path('<str:pk_a>/liked/', pview.LikedView.as_view(), name='get_liked'),
  path('displayName/<str:displayName>', views.getAuthor),
  path('registerNode', views.registerNode.as_view(), name='register_node'),
]

from django.urls import path
from . import views

urlpatterns = [
    path(r'<path:follower>/', views.followers_detail),
    path(r'', views.followers_list),
]

from django.urls import path
from . import views

urlpatterns = [
    path(r'<path:following>/', views.following_detail),
    path(r'', views.following_list),
]

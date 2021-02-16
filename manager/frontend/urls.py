from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('feed', views.index),
    path('post', views.index)
]
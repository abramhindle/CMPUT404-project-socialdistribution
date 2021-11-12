from django.urls import path

from . import views

app_name = 'inbox'
urlpatterns = [
    path('', views.index, name='index'),
    ]
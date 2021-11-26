from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('makepost',views.makepost,name='makepost'),
    path('editpost/<str:post_id>',views.editpost, name='editpost'),
    ]
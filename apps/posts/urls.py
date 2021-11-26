from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('makepost',views.makepost,name='makepost'),
    path('editpost',views.editpost, name='editpost'),
    path('postdetails/<str:post_id>',views.postdetails, name='postdetails'),
    ]
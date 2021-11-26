from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('makepost',views.makepost,name='makepost'),
    path('postdetails/<str:post_id>',views.postdetails, name='postdetails'),
    path('editpost/<str:post_id>',views.editpost, name='editpost'),
    path('deletepost/<str:post_id>',views.deletepost, name='deletepost'),
    ]
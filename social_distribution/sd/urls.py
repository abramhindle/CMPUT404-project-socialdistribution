from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login, name='login'),
    path('create_account', views.create_account, name='create_account'),
    path('requests',views.requests, name='requests'),
    path('author/posts', views.feed, name='private_feed'),
    path('posts', views.explore, name='explore'),
    path('author/<int:author_id>/posts', views.author, name='author_page'),
    path('posts/<int:post_id>', views.post, name='post'),
    path('posts/<int:post_id>/comments', views.post_comment, name='post_comment'),
    path('account', views.account, name='account'),

    # """Optional Pages"""
    # path('search',views.search, name='search'),
    # path('friends', views.friends, name='friends'),

]

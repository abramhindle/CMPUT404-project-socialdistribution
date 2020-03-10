from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url
from .views import *
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),

    url(r'^auth/register/$', CreateAuthorAPIView.as_view(), name='auth_user_create'),
    url(r'^auth/logout/$', AuthorLogoutAPIView.as_view(), name='auth_user_logout'),
    url(r'^auth/login/$', obtain_auth_token, name='auth_user_login'),


    path('login/', auth_views.LoginView.as_view(
        template_name='sd/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='sd/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    path('newpost', views.new_post, name='new_post'),
    path('requests', views.requests, name='requests'),
    path('author/posts', views.feed, name='private_feed'),
    path('posts', views.posts_api_json, name='explore'),
    path('author/<uuid:author_id>/posts', views.author, name='author_page'),
    path('posts/<uuid:post_id>', views.post, name='post'),
    path('posts/<uuid:post_id>/comments',
         views.post_comment, name='post_comment'),
    path('author/<uuid:author_id>/friends', views.friends, name='friends'),

    # """Optional Pages"""
    # path('search',views.search, name='search'),
    path('account', views.account, name='account'),
]

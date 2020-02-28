from django.urls import path

from . import views

urlpatterns = [
    path('login',views.login, name='login'),
    path('create_account', views.create_account, name='create_account'),
    path('forgot_pass',views.forgot_pass, name='forgot_pass'),
    path('home', views.home, name='home'),
    path('search',views.search, name='search'),
    path('friends', views.friends, name='friends'),
    path('requests',views.requests, name='requests'),
    path('account', views.account, name='account'),
]

from django.urls import path

from . import views

app_name = "socialdistribution"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('timeline/', views.timeline, name='timeline'),
    path('profile/', views.profile, name='profile'),
    path('inbox/', views.inbox, name='inbox'),
    path('create-post/', views.CreatePostView.as_view(), name='create-post'),
]
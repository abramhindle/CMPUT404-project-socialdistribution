from django.urls import path
from . import views

urlpatterns = [
    path('<path:path>/', views.get_post, name='get_post'),

    path('', views.get_posts, name='get_posts'),
]
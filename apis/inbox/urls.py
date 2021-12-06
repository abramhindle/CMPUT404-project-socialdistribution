from django.urls import path

from . import views

app_name = 'inbox_api'
urlpatterns = [
    path('inbox', views.inbox.as_view(), name='inbox'),
    path('inbox/', views.inbox.as_view(), name='inbox'),
]
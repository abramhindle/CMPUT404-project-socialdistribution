from django.urls import path

from . import views

app_name = 'inbox_api'
urlpatterns = [
    path('', views.inbox.as_view(), name='inbox'),
]
from django.urls import path
from . import views

urlpatterns = [
    # ex: /posts/
    path('', views.index, name='index'),
    # ex: /posts/5/
]

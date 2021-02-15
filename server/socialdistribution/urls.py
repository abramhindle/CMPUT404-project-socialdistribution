from django.urls import path
from . import views

urlpatterns = [
    path('service/author/', views.register),
    path('service/author/<str:authorID>/', views.author_detail)
]
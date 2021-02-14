from django.urls import path
from . import views

urlpatterns = [
    path('service/author/', views.author_list),
]
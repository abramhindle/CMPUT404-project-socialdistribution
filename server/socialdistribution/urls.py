from django.urls import path
from .api_views import author_view

urlpatterns = [
    path('service/author/', author_view.register),
    path('service/author/<str:authorID>/', author_view.author_detail)
]
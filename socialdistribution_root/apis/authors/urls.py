from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('author/<str:author_id>', views.author.as_view(), name='author'),
    path('authors', views.authors.as_view(), name='authors'),
]
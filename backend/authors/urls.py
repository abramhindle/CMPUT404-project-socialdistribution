from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('<path:path>/', views.get_author, name='get_author'),
    path('', views.get_authors, name='get_authors'),
]

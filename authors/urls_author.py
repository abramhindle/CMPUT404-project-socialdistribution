from django.urls import path, include

from authors import views
from .views import *

urlpatterns = [
    path('', views.author_root, name="author-root"),
    path('<str:author_id>/', AuthorDetail.as_view(), name="author-detail"),
]

from django.urls import path, include

from authors import views
from .views import *

urlpatterns = [
    path('<str:author_id>/', AuthorDetail.as_view(), name="author-detail"),
]

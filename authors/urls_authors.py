from django.urls import path, include

from authors import views
from .views import *

urlpatterns = [
    path('', AuthorList.as_view(), name="author-list"),
]

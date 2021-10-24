from django.conf.urls import url
from django.urls import path, include
from backend.views import *
from network.views import *

urlpatterns = [
    path('', apiOverview, name="apiOverview"),
    path('authors', AuthorList, name ='authorList'),
]

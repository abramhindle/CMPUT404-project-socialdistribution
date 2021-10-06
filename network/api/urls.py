from django.conf.urls import url
from django.urls import path, include
from .views import (
    AuthorListApiView
)

urlpatterns = [
    path('', AuthorListApiView.as_view())
]

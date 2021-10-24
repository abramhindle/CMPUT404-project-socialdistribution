from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('api/',include('network.urls')),
    url('admin/', admin.site.urls),
]

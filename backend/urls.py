from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('',include('network.urls')),
    path('service/',include('network.urls')),
    url('admin/', admin.site.urls),
]

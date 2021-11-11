from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('service/',include('api.urls')),
    path('admin/', admin.site.urls),
]


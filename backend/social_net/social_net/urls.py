from django.urls import include, path
from rest_framework import routers
from API import views
from django.contrib import admin


urlpatterns = [
    # path('', include(router.urls)),
    path('services/', include('API.urls')),
    path('admin/', admin.site.urls),
    # path('^activity/', include('actstream.urls')),
]
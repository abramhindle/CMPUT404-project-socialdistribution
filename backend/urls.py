from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from network.views import *
from backend.views import *

urlpatterns = [
    path('',index,name='index'),
    # path('',include('network.urls')),
    path('service/',include('network.urls')),
    url('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

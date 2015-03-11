from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


from images import views
# Create your views here.


urlpatterns = patterns(
	'images.views',

	url(r'^uploadImage/$', views.upload),
	url(r'^create/$', views.create),

) +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()


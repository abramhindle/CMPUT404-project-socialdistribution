from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^author/', include('post.urls')),
    url(r'^', include('author.urls')),
    url(r'^api/', include('node.urls')),
    url(r'^images/', include('images.urls')),
    url(r'^comment/', include('comment.urls')),
    url(r'^category/', include('category.urls')),
)

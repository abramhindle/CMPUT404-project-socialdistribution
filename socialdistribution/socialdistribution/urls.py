from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socialdistribution.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^author/posts/', include('post.urls')),
    url(r'^', include('author.urls')),
    url(r'^api/', include('node.urls')),
    url(r'^images/', include('images.urls')),
    url(r'^comment/', include('comment.urls')),
)

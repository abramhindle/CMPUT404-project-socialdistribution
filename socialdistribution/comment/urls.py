from django.conf.urls import patterns, include, url

from comment import views
# Create your views here.


urlpatterns = patterns('',
    url(r'^add_comment/$', views.add_comment, name='add_comment'),
    url(r'^remove_comment/(?P<comment_id>\w+)/$', views.remove_comment),
)

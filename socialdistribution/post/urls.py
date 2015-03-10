from django.conf.urls import patterns, include, url

from post import views
# Create your views here.


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<post_id>)\w+/$', views.post, name='post'),
    url(r'(?P<post_id>\d+)/delete/$', views.deletePost),
    # url(r'^(?P<post_id>)/modify/$', views.modifyPost),
    url(r'^create_post$', views.createPost, name='create_post'),
)

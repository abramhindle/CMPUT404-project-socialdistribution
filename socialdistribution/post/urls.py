from django.conf.urls import patterns, include, url

from post import views
# Create your views here.


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^posts/(?P<post_id>\w+/$', views.post, name='post'),
    url(r'^posts/(?P<post_id>/delete/$', views.deletePost, name='delete_post'),
    url(r'^posts/(?P<post_id>/modify/$', views.modifyPost, name='modify_post'),
    url(r'^create_post/$', views.createPost, name='create_post'),
)
from django.conf.urls import patterns, include, url

from post import views
# Create your views here.


urlpatterns = patterns('',
    url(r'^posts/$', views.index, name='index'),
    url(r'^(?P<author_id>[-\w]+)/posts/$', views.posts),
    # url(r'^posts/(?P<post_id>)[-\w]+/$', views.post, name='post'),
    url(r'^posts/(?P<post_id>[-\w]+)/delete/$', views.deletePost, name='delete_post'),
    # url(r'^(?P<post_id>)/modify/$', views.modifyPost),
    url(r'^create_post$', views.createPost, name='create_post'),
)

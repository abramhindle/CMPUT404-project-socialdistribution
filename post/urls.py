from django.conf.urls import patterns, include, url

from post import views
# Create your views here.


urlpatterns = patterns('',
                       url(r'^posts/$', views.index, name='post_index'),
                       url(r'^posts/public/$', views.public, name='public'),
                       url(r'^(?P<author_id>[-\w]+)/posts/$', views.posts, name='user_posts'),
                       url(r'^posts/(?P<tag>\w+)/$', views.taggedPosts, name='tagged_posts'),
                       url(r'^posts/(?P<post_id>[-\w]+)/$', views.post, name='post'),
                       # url(r'^posts/(?P<post_id>)[-\w]+/$', views.post, name='post'),
                       # url(r'^(?P<post_id>)/modify/$', views.modifyPost),
                       )

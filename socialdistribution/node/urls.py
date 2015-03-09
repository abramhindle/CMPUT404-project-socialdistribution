from django.conf.urls import patterns, url

from node import views

urlpatterns = patterns(
    '',
    url(r'^posts/$', views.public_posts),
    url(r'^posts/(?P<post_id>)\d+/$', views.public_posts),
    url(r'^author/posts/$', views.posts),
    url(r'^author/(?P<author>\d+)/posts/$', views.posts),
    url(r'^friends/(?P<user_id>\d+)/$', views.friends),
    url(r'^friends/(?P<user_id1>\d+)/(?P<user_id2>\d+)/$', views.is_friend),
    url(r'^friendrequest/$', views.friend_request),
)

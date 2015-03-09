from django.conf.urls import patterns, url

from node import views

urlpatterns = patterns(
    '',
    url(r'^posts/$', views.all_visible_posts),
    url(r'^posts/(?P<post_id>)\d+/$', views.post),
    url(r'^author/(?P<author>\d+)/$', views.profile),
    url(r'^author/(?P<author>\d+)/posts/$', views.posts),
    url(r'^author/posts/$', views.author_posts),
    url(r'^friends/(?P<user_id>\d+)/$', views.friends),
    url(r'^friends/(?P<user_id1>\d+)/(?P<user_id2>\d+)/$', views.is_friend),
    url(r'^friendrequest/$', views.friend_request),
)

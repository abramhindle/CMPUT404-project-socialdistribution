from django.conf.urls import patterns, url

from author import views

urlpatterns = patterns(
    'author.views',

    url(r'^$', 'login', name='login'),
    #url(r'^register/$', 'register', name='register'),
    url(r'^author/posts/$', views.home),
    url(r'^author/logout/$', views.logout),
    url(r'^author/(?P<author>\d+)/$', views.profile),
    #url(r'^author/(?P<author>\d+)/posts/$', views.other),
)

from django.conf.urls import patterns, url

from author import views

urlpatterns = patterns(
    'author.views',

    url(r'^$', 'login', name='login'),
    #url(r'^logout/$', 'logout', name='logout'),
    #url(r'^register/$', 'register', name='register'),
    url(r'^authors/(?P<author>\d+)/$', views.home),
    url(r'^authors/(?P<author>\d+)/logout/$', views.logout),
)

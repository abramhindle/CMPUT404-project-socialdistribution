from django.conf.urls import patterns, url

urlpatterns = patterns(
    'author.views',

    url(r'^$', 'login', name='login'),
    #url(r'^logout/$', 'logout', name='logout'),
    #url(r'^register/$', 'register', name='register'),
)

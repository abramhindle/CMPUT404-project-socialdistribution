from django.conf.urls import patterns, include, url

from comment import views
# Create your views here.


urlpatterns = patterns('',
                       url(r'^', views.comment, name='comment_index'),
                       )

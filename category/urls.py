from django.conf.urls import patterns, include, url

from category import views
# Create your views here.


urlpatterns = patterns('category.views',
 						url(r'^index/$', views.index, name='category_index'),
                       )

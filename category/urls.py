from django.conf.urls import patterns, include, url

from category import views
# Create your views here.


urlpatterns = patterns('category.views',
 						url(r'^index/$', views.index,name='index'),
 						url(r'^category/$',views.categories,name='categories'),
 						url(r'^category/(?P<category_name>\w+)/$',views.category,name='category'),
						url(r'^post_with_category/$', views.postcategory ,name='postcategory'),
						#url(r'^add$', views.add),
						#url(r'^delete$', views.remove),
                       )

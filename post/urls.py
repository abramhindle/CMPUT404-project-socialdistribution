from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    # /post/
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /post/71/
    #url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /post/add/
    url(r'add/$', views.PostCreate.as_view(), name='post-add'),


    #This is to update post. Currently not set-up in the front-end
    # /post/71/
    url(r'(?P<pk>[0-9]+)/$', views.PostUpdate.as_view(), name='post-update'),


    # /post/71/delete/
    url(r'(?P<pk>[0-9]+)/delete/$', views.PostDelete.as_view(), name='post-delete'),
]
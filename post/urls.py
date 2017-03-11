from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    # /post/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /post/71/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /post/add/
    url(r'^add/$', views.post_create, name='post-add'),

    # This is to update post. Currently not set-up in the front-end
    # /post/71/
    url(r'(?P<pk>[0-9]+)/$', views.PostUpdate.as_view(), name='post-update'),

    # /post/71/delete/
    url(r'(?P<pk>[0-9]+)/delete/$', views.PostDelete.as_view(), name='post-delete'),

    # /post/71/comment
    url(r'(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]

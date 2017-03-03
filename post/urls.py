from django.conf.urls import url
from . import views

urlpatterns = [
    # /post/
    url(r'^$', views.index, name='index'),

    # /post/71/
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
]
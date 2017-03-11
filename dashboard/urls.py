from django.conf.urls import url
from django.views.generic import TemplateView

from dashboard import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='dashboard/index.html'), name='index'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='author-list'),
    url(r'^authors/(?P<pk>[0-9]+)$', views.AuthorDetailView.as_view(), name='author-detail'),
]

from django.conf.urls import url
from django.views.generic import TemplateView

from dashboard import views
from dashboard import views as dashboard_views

urlpatterns = [
    url(r'^$', dashboard_views.index, name='index'),
]

from django.conf.urls import url
from django.views.generic import TemplateView

from dashboard import views

urlpatterns = [
    url(r'^403$', TemplateView.as_view(template_name='403.html')),
    url(r'^404$', TemplateView.as_view(template_name='404.html')),
    url(r'^500$', TemplateView.as_view(template_name='500.html')),
]

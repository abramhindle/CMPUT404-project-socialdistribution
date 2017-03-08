from django.conf.urls import url
from django.views.generic import TemplateView

from dashboard import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='dashboard/index.html'), name='index'),

]

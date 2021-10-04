from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

# Serves a SPA
index = never_cache(TemplateView.as_view(template_name='index.html'))
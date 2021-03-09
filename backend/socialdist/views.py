from django.views.generic import TemplateView

# Serve Single Page Application
index = TemplateView.as_view(template_name='index.html')

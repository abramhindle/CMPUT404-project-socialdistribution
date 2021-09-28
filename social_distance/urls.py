"""social_distance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import api_root
from authors import views as authors_view
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

schema_view = get_schema_view(title='social-distance API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # authors app
    path('authors/', include('authors.urls_authors')),
    path('author/', include('authors.urls_author')),

    # root
    path('schema/', schema_view, name='open-schema'),
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'open-schema'}
    ), name='swagger-ui'),

    # TODO login, logout, register
]


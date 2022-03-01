"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views


urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),

    # List All Authors On The Local Server
    path('authors/', views.get_authors, name='get_authors'),

    # Proxy Requests Either To The Local Server Or To Other Servers In The Network
    path('authors/<path:path>/', views.proxy_requests, name='proxy_requests'),

    # Inbox API
    path('api/authors/<uuid:author>/inbox/', include('inbox.urls')),

    # Author API
    path('api/authors/', include('authors.urls')),

    # Post API
    path('api/authors/<uuid:author>/posts/', include('posts.urls')),

    # Serve API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Serve Swagger Docs
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

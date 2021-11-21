"""Social_Distribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from django.shortcuts import render
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


router = routers.DefaultRouter()


def render_react(request, data):
    return render(request, "index.html")

urlpatterns = [
    path('service/author/<str:author_id>/', include('post.urls')),
    path('service/', include('author.urls')),
    path('service/internal/', include('server.urls')),
    path('admin/', admin.site.urls),
    staticfiles_urlpatterns()[0],
    re_path(r"^(?!service|admin|static)(.*)$", render_react),

    #path('', include(router.urls)),
    #path('api/', include('rest_framework.urls', namespace='rest_framework')),
    #path('accounts/', include('django.contrib.auth.urls'))
]

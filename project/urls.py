"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from landing.views import index as landing_index

urlpatterns = [
    url(r'^$', landing_index, name='landing'),
    url(r'^admin/', admin.site.urls),
    url(r'^post/', include('post.urls')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^accounts/logout/$', auth_views.logout),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout, name='logout'),
]

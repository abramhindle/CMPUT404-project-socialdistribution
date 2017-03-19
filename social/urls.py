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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from registration.backends.simple.views import RegistrationView
from social.app import urls as debug_urls
from social.app.views import author as author_views
from service import urls as rest_api_urls
from social.app.forms.user_profile import UserProfileForm
from . import settings

urlpatterns = [
    url(r'^service/', include(rest_api_urls.urlpatterns, namespace='service')),
    url(r'^admin/', admin.site.urls, name='admin'),

    url(r'^', include('social.app.urls', namespace='app')),
    url(r'^accounts/logout/$', auth_views.logout),
    url(r'^accounts/activation$',
        login_required(TemplateView.as_view(template_name='account/activation_required.html')),
        name='activation_required'),
    url(r'^accounts/register/$',
        RegistrationView.as_view(
            form_class=UserProfileForm
        ),
        name='registration_register',
        ),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/(?P<pk>[\-\w]+)/$', author_views.edit_user, name='account_update'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^debug/', include(debug_urls.urlpatterns, namespace='debug')),
]

admin.site.site_header = 'Social Distribution Administration'
admin.site.site_title = 'Social Distribution site admin'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

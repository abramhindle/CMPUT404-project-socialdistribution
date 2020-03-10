"""socialdistribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from profiles import views as profiles_views
from socialdistribution import views as socialdistribution_views
from django_registration.backends.one_step.views import RegistrationView
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', profiles_views.index, name='index'),
    path('404/', socialdistribution_views.error_404, name='error_404'),
    path('403/', socialdistribution_views.error_403, name='error_403'),
    path('500/', socialdistribution_views.error_500, name='error_500'),
    path('new_post/', include('profiles.urls')),
    path('stream/', include('posts.urls')),
    path('editprofile/', profiles_views.edit_profile, name='editprofile'),
    path('viewprofile/', profiles_views.view_profile, name='viewprofile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', profiles_views.register, name = "register"),
    path('api/', include('api.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

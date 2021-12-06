"""socialdistribution URL Configuration

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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from socialdistribution import views

schema_view = get_schema_view(
   openapi.Info(
      title="T18 Social Distrivution API",
      default_version='v1',
      description="Documentation for T18 Social Distribution project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@dummy.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('author/<str:author_id>/', include('apis.likes.urls')),
    path('author/<path:author_id>/posts/', include('apis.posts.urls')),
    path('author/<path:author_id>/', include('apis.inbox.urls')),
    path('admin/', admin.site.urls),
    path('site/posts/', include('apps.posts.urls')),
    # path('site/accounts/', include('django.contrib.auth.urls')), #this handles user authentication
    path('', include('apis.authors.urls')),
    path('site/inbox/',include('apps.inbox.urls')),
    path('', include('apps.core.urls')),
    url(r'^playground/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # auth
    path('site/accounts/logout/', views.LogoutView.as_view(), name="logout"),
    path('site/accounts/login/', views.LoginView.as_view(), name="login"),
    path('site/accounts/password_reset_complete/', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('site/accounts/password_reset_confirm/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('site/accounts/password_reset_done/', views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('site/accounts/password_reset/', views.PasswordResetView.as_view(), name="password_reset"),
]

handler404 = views.error_404
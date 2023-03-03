"""social_distribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework.schemas import get_schema_view
from apps.authors.views import authors_paginated
from apps.posts.views import Post_All


urlpatterns = [

    path('admin/', admin.site.urls),                                # Django admin site
    path('api-auth/', include('rest_framework.urls')),              # Prefix for API login and logout
    path('api-schema/', get_schema_view(), name='API Schema'),      # API schema endpoint (used for dynamic swagger docs generation)
    path('docs/', include('apps.docs.urls')),                       # Prefix for documentation pages (currently /docs/api/ only)
    path('authors/', include('apps.authors.urls')),                 # Pretty much every other URI starts with this author prefix
    path('authors', authors_paginated, name='Authors Paginated'),   # Project spec indicates there shouldn't be a trailing slash on paginated authors, so here it is
    path('posts/', Post_All.as_view(), name='TEST URL FOR POSTS')   # Test url for posts
]

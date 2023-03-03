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
from django.urls import include, path
from apps.posts.views import posts_paginated
from apps.authors.views import all_authors, single_author
from .views import Author_Individual, Author_All, Author_Post


urlpatterns = [
    path('', Author_All.as_view(), name="All Authors"),
    path('<str:author_id>/posts/', Author_Post.as_view(), name="Author's posts"),
    path('<str:author_id>/posts/', posts_paginated, name="Posts Paginated"),
    path('<str:author_id>/', Author_Individual.as_view(), name="Single Author"),

]

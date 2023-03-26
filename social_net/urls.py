from django.urls import include, path, re_path
from rest_framework import routers
from API import views
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,   # TODO: Possibly make this false. Assignment specs says stuff like 'gib public api docs' but I don't think it's referring to this, and limiting what people can see to only the things they can access sounds more useful to other nodes and more secure too.
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # path('', include(router.urls)),
    path('service/', include('API.urls')),     # CHANGED: "services/" to "service/" (singular, not plural)
    path('admin/', admin.site.urls),
    # path('^activity/', include('actstream.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
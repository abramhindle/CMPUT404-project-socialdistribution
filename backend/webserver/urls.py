from django.urls import path,include

from .views import(
    AuthorView,
)

#from . import views
#from rest_framework import routers

#router = routers.DefaultRouter()
# first argument, endpoint, second argument is the view that calling the url will send the request to
#router.register('authors',views.AuthorView)
urlpatterns = [
    path('api',AuthorView.as_view())
    #path('',include(router.urls))
]
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer

from api.serializers import AuthorSerializer
from api.util import page_number_pagination_class_factory


class AuthorViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    pagination_class = page_number_pagination_class_factory([('type', 'authors')])

    queryset = get_user_model().objects.filter(is_active=True, is_staff=False, is_api_user=False).order_by('id')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

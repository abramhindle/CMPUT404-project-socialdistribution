from django.contrib.auth.models import User
from rest_framework import viewsets

from service.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

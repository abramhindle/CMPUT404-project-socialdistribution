from rest_framework import viewsets, permissions

from .models import DummyPost
from .serializers import DummyPostSerializer


class DummyPostViewSet(viewsets.ModelViewSet):
    queryset = DummyPost.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = DummyPostSerializer
from rest_framework import viewsets, permissions

from .models import DummyPost
from .serializers import DummyPostSerializer


class DummyPostViewSet(viewsets.ModelViewSet):
    queryset = DummyPost.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = DummyPostSerializer
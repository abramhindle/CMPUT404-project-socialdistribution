from django.shortcuts import render
from rest_framework import viewsets
from .models import Node
from .serializers import NodeSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

# Create your views here.
class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    permission_classes = [IsAdminUser]
    queryset = Node.objects.all()


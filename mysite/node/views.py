from django.shortcuts import render
from rest_framework import viewsets
from .models import Node
from .serializers import NodeSerializer

# Create your views here.
class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()


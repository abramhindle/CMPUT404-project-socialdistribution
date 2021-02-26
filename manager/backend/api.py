from backend.models import Author
from rest_framework import viewsets, permissions
from .serializers import AuthorSerializer

# Author Viewset
class AuthorViewSet(viewsets.ModelViewSet):
    
    queryset = Author.objects.all()

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AuthorSerializer

    lookup_field = 'id'
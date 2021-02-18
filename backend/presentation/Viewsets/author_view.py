from presentation.models import Author
from django.shortcuts import get_object_or_404
from presentation.Serializers.author_sereializer import AuthorSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

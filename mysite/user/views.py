from django.shortcuts import render
from .serializers import AuthorSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer

    # add authentication to this view
    # user can only use this view with valid token
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()

    # used to get user detail by their username
    lookup_field = 'username'

    # only return the records of author
    def get_queryset(self):
        return self.queryset.filter(is_superuser=0)

    # used to update the author's profile
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AuthorSerializer(instance=instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from social_net.API.serializers import UserSerializer, GroupSerializer, AuthorSerializer
from rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(request, format=None):
        
        queryset = User.objects.all().order_by('-date_joined')
        serializer_class = AuthorSerializer
        permission_classes = [permissions.IsAuthenticated]
        
        queryset = User.objects.all().order_by('-date_joined')
        serializer_class = UserSerializer
    
    def post(request, format=None):
        
        queryset = User.objects.all().order_by('-date_joined')
        serializer_class = AuthorSerializer.get(validated_data)
        permission_classes = [permissions.IsAuthenticated]

    # permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
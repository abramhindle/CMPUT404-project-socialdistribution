from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import CommonAuthenticateSerializer, RegisterSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authors': reverse('author-list', request=request, format=format),
        'author': reverse('author-root', request=request, format=format),
    })


# TODO: login, logout, register. bind User and Author
@extend_schema(
    request=RegisterSerializer,
    responses=CommonAuthenticateSerializer
)
@api_view(['POST'])
def register(request):
    # deserialize request data
    serializer = RegisterSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        # create user and author
        user = serializer.save()
        return Response(CommonAuthenticateSerializer(user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=CommonAuthenticateSerializer,
    responses=CommonAuthenticateSerializer
)
@api_view(['POST'])
def login(request):
    serializer = CommonAuthenticateSerializer(data=request.data)
    print(serializer.initial_data, serializer.is_valid(), serializer.errors)
    if serializer.is_valid():
        data = serializer.validated_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(CommonAuthenticateSerializer(user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

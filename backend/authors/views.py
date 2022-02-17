from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import action
from django.db.utils import IntegrityError
from .models import Author
from django.contrib.auth.models import User
from .serializers import AuthorSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib import auth
from rest_framework.authtoken.models import Token


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "authors", 'items': data})


class AuthorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = CustomPageNumberPagination

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            user = User.objects.create_user(username=request.data["displayName"], password=request.data["password"])
            author = user.author
            author.github = "https://www.github.com/" + request.data["github"]
            author.save()
            return Response(AuthorSerializer(author).data)
        except IntegrityError:
            return Response({"error": "Username Already Exists!"}, status=status.HTTP_409_CONFLICT)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        user = auth.authenticate(username=request.data["displayName"], password=request.data["password"])
        if user is not None:
            author = user.author
            if author.verified:
                auth.login(request, user)
                response = {'message': 'Successfully Logged In!', 'author': AuthorSerializer(author).data, 'token': Token.objects.get_or_create(user=user)[0].key }
                return Response(response, status=status.HTTP_200_OK)
            return Response({"error": "Your Account Is Awaiting Approval By The Admin!"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Invalid Username Or Password!"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        user: User = request.user
        user.auth_token.delete()
        return Response({"message": "Succesfully Logged Out!"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['login']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

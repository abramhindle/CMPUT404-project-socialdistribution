import base64
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.decorators import action, renderer_classes
from django.db.utils import IntegrityError
from .models import Author, Avatar
from django.contrib.auth.models import User
from .serializers import AuthorSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib import auth
from rest_framework.authtoken.models import Token
from likes.models import Likes
from likes.serializers import LikesSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({'type': "authors", 'items': data})


class AuthorViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by("displayName")
    pagination_class = CustomPageNumberPagination

    @action(detail=True, methods=['GET'])
    def liked(self, request, pk):
        author: Author = get_object_or_404(Author, local_id=pk)
        likes = Likes.objects.all().filter(author_url=author.id)
        return Response({"type": "liked", "items": LikesSerializer(likes, many=True).data}, content_type="application/json")

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

    @action(detail=True, methods=['GET', 'PATCH'])
    def avatar(self, request, pk):
        author: Author = get_object_or_404(Author, local_id=pk)
        avatar: Avatar = author.avatar
        if request.method == "GET":
            string = avatar.content
            content = string.split("base64,")[1]
            mimetype = string.split(";base64,")[0].split(":")[1]
            response = HttpResponse(content_type=mimetype)
            response.write(base64.b64decode(content))
            return response
        avatar.content = request.data["content"]
        avatar.save()
        return Response({"ok": "Successfully Changed Avatar!"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Manages Permissions On A Per-Action Basis"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

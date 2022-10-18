from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer, AuthorRegistrationSerializer
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import status, permissions

class AuthorsView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
        

class AuthorDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_author(self,pk):
        author = get_object_or_404(Author,pk=pk)
        return author

    
    def get(self, request, pk, *args, **kwargs):
        author = self.get_author(pk)
        serializer = AuthorSerializer(author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request, pk, *args, **kwargs):
        author = self.get_author(pk)
        serializer = AuthorSerializer(instance=author, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorRegistrationView(APIView):
    def post(self, request):
        serializer = AuthorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'message': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login Success'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

      
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully Logged out'}, status=status.HTTP_200_OK)

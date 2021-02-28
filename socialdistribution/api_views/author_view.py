from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from socialdistribution.models import Author
from socialdistribution.serializers import RegistrationSerializer, AuthorSerializer

@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid(): # make sure data match the model
        author = serializer.save()
        return Response({'authorID':author.authorID}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message':serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['GET', 'POST'])
def author_detail(request, authorID):
    if request.method == "GET":
        # get author data
        author = get_object_or_404(Author, authorID=authorID)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        author = get_object_or_404(Author, authorID=authorID)
        serializer = AuthorSerializer(author, data=data)
        if serializer.is_valid():
            if "password" in data:
                author.set_password(data['password'])
            if 'username' in data:
                author.username = data['username']
            if 'email' in data:
                new_email = data['email'].lower()
                # check new email doesn't already exists
                if author.email != new_email and Author.objects.filter(email=new_email).exists():
                    return Response({'message':'email already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                author.email = new_email
            author.save()
            serializer.save()
            return Response({'message':'Updated Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    user = authenticate(email=request.data['email'].lower(), password=request.data['password'])
    if user is not None:
        return Response({'authorID':user.authorID}, status=status.HTTP_200_OK)
    else:
        return Response({'message':"incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def logout_view(request):
    return redirect("http://localhost:3000/")
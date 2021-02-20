from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, logout
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

    # elif request.method == "POST":
    #     serializer = AuthorSerializer(data=request.data)
    #     if serializer.is_valid(): # make sure data match the model
    #         serializer.save()
    #         data = {"count": 333, 'adf': "dafa"}
    #         return Response(data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    user = authenticate(email=request.data['email'].lower(), password=request.data['password'])
    if user is not None:
        return Response({'authorID':user.authorID}, status=status.HTTP_200_OK)
    else:
        return Response({'message':"incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def logout_view(request):
    logout(request);
    return redirect("http://localhost:3000/")
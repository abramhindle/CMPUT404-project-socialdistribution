from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import status
from socialdistribution.models import Author
from socialdistribution.serializers import RegistrationSerializer, AuthorSerializer


@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid(): # make sure data match the model
        author = serializer.save()
        data['authorID'] = author.authorID
        return JsonResponse(data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET', 'POST'])
def author_detail(request, authorID):
    if request.method == "GET":
        author = get_object_or_404(Author, authorID=authorID)

        serializer = AuthorSerializer(author)
        return JsonResponse(serializer.data, safe=False)

    # elif request.method == "POST":
    #     serializer = AuthorSerializer(data=request.data)
    #     if serializer.is_valid(): # make sure data match the model
    #         serializer.save()
    #         data = {"count": 333, 'adf': "dafa"}
    #         return JsonResponse(data, status=status.HTTP_201_CREATED)
    #     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    user = authenticate(email=request.data['email'].lower(), password=request.data['password'])
    data = {}
    if user is not None:
        data['authorID'] = user.authorID
        return JsonResponse(data, status=status.HTTP_200_OK)
    else:
        return JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)



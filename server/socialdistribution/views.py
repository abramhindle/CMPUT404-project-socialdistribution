from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Author
from .serializers import AuthorSerializer


@api_view(['GET', 'POST'])
def author_list(request):
    if request.method == "GET":
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid(): # make sure data match the model
            serializer.save()
            data = {"count": 333, 'adf': "dafa"}
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def author_detail(request, pk):
#     if request.method == "GET":
#         try:
#             author = Author.objects.get(pk=pk)
#         except:
#             return JsonResponse(status=status.HTTP_404_NOT_FOUND)

#         serializer = AuthorSerializer(author)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == "POST":
#         serializer = AuthorSerializer(data=request.data)
#         if serializer.is_valid(): # make sure data match the model
#             serializer.save()
#             data = {"count": 333, 'adf': "dafa"}
#             return JsonResponse(data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def Post(request):
    return HttpResponse("<h1> posssssssstT</h1>")

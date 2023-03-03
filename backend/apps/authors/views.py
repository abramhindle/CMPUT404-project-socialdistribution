from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Author
from apps.posts.models import Post
from django.http import Http404
from .serializers import AuthorSerializer
from apps.posts.serializers import PostSerializer
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.


@api_view(['GET'])
def authors_paginated(request: Request, page: int = 10, size: int = 5):
    """
    /authors?page=10&size=5

    GET (local, remote): retrieve all profiles on the server (paginated) 
    """
    page = request.GET.get('page', '')
    size = request.GET.get('size', '')

    if page == '':
        page = 10
    if size == '':
        size = 5

    try:
        page = int(page)
        assert page > 0
    except Exception as e:
        page = 10

    try:
        size = int(size)
        assert size > 0
    except Exception as e:
        size = 5

    return Response({"message": f"Viewing {page} pages with {size} authors per page"})


# @api_view(['GET'])
# def all_authors(request: Request):
#     """
#     /authors/

#     GET (local, remote): Used to view all authors
#     """
#     return Response({"message": "Viewing all authors"})


class Author_All(APIView):

    def get(self, request, format=None):
        """
        /authors/

        GET (local, remote): Used to view all authors
        """
        query_set = Author.objects.all()
        serializer = AuthorSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        /authors/

        POST (test): Used to create an author (put author_id in the json)
        """
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'POST'])
# def single_author(request: Request, author_id: str):
#     """
#     /authors/{author_id}/

#     GET (local, remote): retrieve AUTHOR_ID profile

#     POST (local): update AUTHOR_ID profile
#     """

#     if request.method == 'GET':
#         return Response({"message": f"Viewing author {author_id}"})

#     elif request.method == 'POST':
#         return Response({"message": f"Updating author {author_id}"})


class Author_Individual(APIView):

    def get_object(self, id, format=None):
        """
        Gets a query from the database.
        """
        try:
            return Author.objects.get(id=id)
        except:
            Author.DoesNotExist
            raise Http404

    def get(self, request, author_id, format=None):
        """
        /authors/{author_id}/
        
        GET (local, remote): retrieve AUTHOR_ID profile
        """
        query = self.get_object(author_id)
        serializer = AuthorSerializer(query)
        return Response(serializer.data)

    def post(self, request, author_id, format=None):
        """
        /authors/{author_id}/
        
        POST (local): update AUTHOR_ID profile
        """
        query = self.get_object(author_id)
        serializer = AuthorSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    ALERT
    When you POST author with the id, you have to pass the id inside the json. 

    Example - 
    url: http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e
    id: 9de17f29c12e8f97bcbbd34cc908f1baba40658e
    """

    # def post(self, request, author_id, format=None):
    #     obj = Author_All
    #     Author_All.post(request)


# class Author_Post(APIView):

#     def get_object(self, id, format=None):
#         """
#         Gets a query from the database.
#         """
#         query_set = Post.objects.filter(author_id__pk=id)
#         if query_set:
#             return query_set
#         raise Http404

#     def get(self, request, author_id, format=None):
#         """
#         GET baseurl/authors/<author_id>/posts/
#         """
#         query = self.get_object(author_id)
#         serializer = PostSerializer(query, many=True)
#         return Response(serializer.data)

#     def post(self, request, author_id, format=None):
#         """
#         POST baseurl/authors/<authors_id>/posts/
#         You have to put the post_id in the json.
#         """
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



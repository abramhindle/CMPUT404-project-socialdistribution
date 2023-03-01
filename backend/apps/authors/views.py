from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

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


@api_view(['GET'])
def all_authors(request: Request):
    """
    /authors/

    GET (local, remote): Used to view all authors
    """
    return Response({"message": "Viewing all authors"})


@api_view(['GET', 'POST'])
def single_author(request: Request, author_id: str):
    """
    /authors/{author_id}/

    GET (local, remote): retrieve AUTHOR_ID profile

    POST (local): update AUTHOR_ID profile
    """

    if request.method == 'GET':
        return Response({"message": f"Viewing author {author_id}"})

    elif request.method == 'POST':
        return Response({"message": f"Updating author {author_id}"})

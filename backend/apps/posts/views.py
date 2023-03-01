from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.


@api_view(['GET'])
def posts_paginated(request: Request, author_id: str, page: int = 10, size: int = 5):
    """
    /authors/{AUTHOR_ID}/posts?page=10&size=5

    GET (local, remote) get the recent posts from author AUTHOR_ID (paginated)
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

    return Response({"message": f"Viewing {page} pages with {size} posts per page for author {author_id}"})


@api_view(['GET', 'POST'])
def all_posts(request: Request, author_id: str):
    """
    /authors/{author_id}/posts/

    GET (local, remote) Used to view all posts from a particular author

    POST (local) create a new post but generate a new id
    """

    if request.method == 'GET':
        return Response({"message": f"Viewing all posts for author {author_id}"})
    
    elif request.method == 'POST':
        return Response({"message": f"Creating a new post for author {author_id}"})


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def single_post(request: Request, author_id: str, post_id: str):
    """
    /authors/{author_id}/posts/{post_id}

    GET (local, remote) get the public post whose id is POST_ID

    POST (local) update the post whose id is POST_ID (must be authenticated)

    DELETE (local) remove the post whose id is POST_ID

    PUT (local) create a post where its id is POST_ID
    """

    if request.method == 'GET':
        return Response({"message": f"Viewing single post {post_id} from author {author_id}"})
    elif request.method == 'POST':
        return Response({"message": f"Updating single post {post_id} from author {author_id}"})
    elif request.method == 'DELETE':
        return Response({"message": f"Removing single post {post_id} from author {author_id}"})
    elif request.method == 'PUT':
        return Response({"message": f"Creating single post {post_id} from author {author_id}"})
    

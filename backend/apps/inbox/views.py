from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.
@api_view(['GET'])
def inbox(request: Request, author_id: str):
    """
    /inbox

    GET (local, remote): retrieve AUTHOR_ID profile

    """

    return Response({"message": "Viewing all Inbox Notifications"})

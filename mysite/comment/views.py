from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action

from user.models import User
from .models import Comment
from comment.serializer import CommentSerializer
from .serializers import PostSerializer
from .models import Post, VISIBILITYCHOICES
from .permissions import OwnerPermissions

# @api_view(['POST'])
# def post(request):

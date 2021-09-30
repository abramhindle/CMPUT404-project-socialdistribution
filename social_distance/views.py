from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from drf_spectacular.utils import extend_schema

from authors.models import Author
from authors.serializers import AuthorSerializer
from .serializers import RegisterSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authors': reverse('author-list', request=request, format=format),
        'author': reverse('author-root', request=request, format=format),
    })


# TODO: login, logout, register. bind User and Author
@extend_schema(
    request=RegisterSerializer,
    responses=AuthorSerializer,
)
@api_view(['POST'])
def register(request):
    # deserialize request data
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        # create user
        user = serializer.save()
        # TODO: if register approval turned on, set user.is_active = False

        data = serializer.validated_data
        # create author and link with user
        author = Author(user=user, display_name=data.get('display_name', user.username), github_url=data.get('github_url'))
        # modify url to be server path
        author.update_fields_with_request(request)

        author_response_serializer = AuthorSerializer(author)
        return Response(author_response_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema

from .serializers import AuthorSerializer

from .models import Author
# Create your views here.

# https://www.django-rest-framework.org/tutorial/3-class-based-views/
class AuthorList(APIView):
    """
    List all authors in this server.
    """
    @extend_schema(
        responses=AuthorSerializer(many=True), # specify response format for list: https://drf-spectacular.readthedocs.io/en/latest/faq.html?highlight=list#i-m-using-action-detail-false-but-the-response-schema-is-not-a-list
    )
    def get(self, request):
        authors = Author.objects.all() 
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class AuthorDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        # used for schema generation for all methods
        # https://drf-spectacular.readthedocs.io/en/latest/customization.html#step-1-queryset-and-serializer-class
        return AuthorSerializer

    """
    Get author profile
    """
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)

    """
    Update author profile
    """
    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            author = serializer.save()
            # modify url to be server path
            author.update_fields_with_request(request)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def inbox(request, author_id):
    return Response({'msg': 'ok'})

@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def internally_send_friend_request(request, author_id, foreign_author_url):
    import requests

    try:
        author = Author.objects.get(id=author_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get that foreign author
    foreign_author_json = requests.get(foreign_author_url).json()

    # TODO do we check for foreign author validity?

    friend_request_payload = {
        'type': 'Follow',
        'summary': f"{author.display_name} wants to follow {foreign_author_json.get('displayName')}", # TODO
        'actor': AuthorSerializer(author).data,
        'object': foreign_author_json,
    }
    res = requests.post(foreign_author_url + 'inbox/', json=friend_request_payload).json()

    return Response({'debug_foreign_author_url': foreign_author_url, 'debug_author_id': author_id, 'debug_foreign_response': res, 'req': friend_request_payload})
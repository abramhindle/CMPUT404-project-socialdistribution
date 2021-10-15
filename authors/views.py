from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import exceptions, status, permissions
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema

from .serializers import AuthorSerializer, FriendRequestSerializer, InboxObjectSerializer

from .models import Author, InboxObject
# Create your views here.

# https://www.django-rest-framework.org/tutorial/3-class-based-views/


class AuthorList(APIView):
    """
    List all authors in this server.
    """
    @extend_schema(
        # specify response format for list: https://drf-spectacular.readthedocs.io/en/latest/faq.html?highlight=list#i-m-using-action-detail-false-but-the-response-schema-is-not-a-list
        responses=AuthorSerializer(many=True),
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


class InboxListView(ListCreateAPIView):
    """
    POST to inbox: a foreign server sends some json object to the inbox. server basic auth required
    GET from inbox: get all objects for the current user. user jwt auth required
    """
    # permission_classes = [permissions.permissions.IsAuthenticated]
    serializer_class = InboxObjectSerializer

    def get_serializer_context(self):
        # append the endpoint author to the serializer context
        # the serializer will use it for creating an InboxObject.
        try:
            author = Author.objects.get(id=self.kwargs.get('author_id'))
        except:
            raise exceptions.NotFound
        return {
            'author': author
        }

    def get_queryset(self):
        try:
            author = Author.objects.get(id=self.kwargs.get('author_id'))
        except:
            raise exceptions.NotFound
        return author.inbox_objects.all()


@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def internally_send_friend_request(request, author_id, foreign_author_url):
    """
    the /author/<author_id>/friend_request/<foreign_author_url>/ endpoint
    - author_id: anything other than slash, but we hope it's a uuid
    - foreign_author_url: anything, but we hope it's a valid url.

    used only by local users, jwt authentication required.
    Its job is to fire a POST to the foreign author's inbox with a FriendRequest json object.

    NOTE: I think putting url inside a url sucks, too. -Lucas

    questions:
    - what to expect from POST result?
    - How do we know the friend request has been accepted?
    """
    import requests

    try:
        author = Author.objects.get(id=author_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get that foreign author's json object first
    foreign_author_json = requests.get(foreign_author_url).json()

    # TODO do we check for foreign author validity?

    friend_request_payload = {
        'type': 'Follow',
        # TODO
        'summary': f"{author.display_name} wants to follow {foreign_author_json.get('displayName')}",
        'actor': AuthorSerializer(author).data,
        'object': foreign_author_json,
    }
    res = requests.post(foreign_author_url + 'inbox/',
                        json=friend_request_payload).json()
    return Response({'debug_foreign_author_url': foreign_author_url, 'debug_author_id': author_id, 'debug_foreign_response': res, 'req': friend_request_payload})

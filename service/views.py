from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from service.serializers import UserSerializer, AuthorSerializer, FriendRequestSerializer
from dashboard.models import Author


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def send_friend_request(request):
    serializer = FriendRequestSerializer(data=request.data)

    if serializer.is_valid():
        friend_request = serializer.save()

        # TODO: Add code to handle case when one or more users are remote
        author_id = friend_request.author.get_id_without_url()
        friend_id = friend_request.friend.get_id_without_url()

        author = Author.objects.get(id=author_id)

        # TODO: Allow for case where remote server submitted this on behalf of another user
        if author.user_id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        friend = Author.objects.get(id=friend_id)

        author.outgoing_friend_requests.add(friend)
        author.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

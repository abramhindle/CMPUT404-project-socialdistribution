from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, detail_route
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
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=["POST"])
    def follow(self, request, pk=None):

        follower = request.user.profile

        if not follower.activated:
            return Response(
                {"detail": "Unactivated authors cannot follow other authors."},
                status=status.HTTP_403_FORBIDDEN)

        try:
            followee = Author.objects.get(id=pk)
        except Author.DoesNotExist:
            return Response(
                {'detail': 'The author you wanted to follow could not be found.'},
                status=status.HTTP_404_NOT_FOUND)

        # Does this author already follow followee?
        if follower.followed_authors.filter(id=followee.id):
            return Response(
                {"detail": "You already follow this author."},
                status=status.HTTP_403_FORBIDDEN)

        if not followee.activated:
            return Response(
                {"detail": "Unactivated authors cannot be followed."},
                status=status.HTTP_403_FORBIDDEN)

        follower.followed_authors.add(followee)

        return Response(
            {"followed_author": followee.get_id_url()},
            status=status.HTTP_200_OK)


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
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

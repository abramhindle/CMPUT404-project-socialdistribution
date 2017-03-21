from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from service.friendrequest.serializers import FriendRequestSerializer
from social.app.models.author import Author


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def friendrequest(request):
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

        author.add_friend_request(friend)
        author.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
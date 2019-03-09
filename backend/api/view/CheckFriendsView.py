from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Follow


class CheckFriendsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return None

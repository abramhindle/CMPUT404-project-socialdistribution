from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Post
from ..serializers import PostSerializer

class GetPostsView(generics.GenericAPIView):
    serializer_class = AuthorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, authorid):
        pass
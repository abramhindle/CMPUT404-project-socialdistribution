from rest_framework.views import APIView
from rest_framework.response import Response
from service.models.likes import Likes
from service.serializers.likes import LikesSerializer
import json

class LikesView(APIView):
    serializer_class = LikesSerializer

    def get(self, request, author, post, comment=None):

        if not comment:
            likes_query = Likes.objects.filter(object = post)
        else:
            likes_query = Likes.objects.filter(object = comment)
        likes = self.serializer_class(likes_query, many=True).data

        return Response({"likes": json.dumps(likes)}, status=200)
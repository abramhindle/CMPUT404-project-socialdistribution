from rest_framework.views import APIView
from rest_framework.response import Response
from service.models.liked import Liked
from service.models.author import Author
from service.serializers.liked import LikedSerializer
import json


class LikedView(APIView):
    serializer_class = LikedSerializer

    def get(self, request, author):
        author_query = Author.objects.get(_id = author)
        liked = Liked.objects.filter(items__author = str(author_query._id))[0] # would be better to add author_id field into Liked model, so it takes less resources to querying
        
        return Response({"liked": json.dumps(self.serializer_class(liked).data)})
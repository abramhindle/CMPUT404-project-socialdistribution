from rest_framework.views import APIView
from rest_framework.response import Response
from service.models.likes import Likes
from service.models.liked import Liked
from service.models.author import Author
from service.serializers.liked import LikedSerializer


class LikedView(APIView):
    serializer_class = LikedSerializer

    def get(self, request, author):
        author_query = Author.objects.get(_id = author)
        liked = Liked.objects.create()

        liked.items.set(Likes.objects.filter(author = str(author_query._id)))
        
        return Response({"liked": self.serializer_class(liked).data})
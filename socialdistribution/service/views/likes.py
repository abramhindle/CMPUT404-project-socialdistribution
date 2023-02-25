from rest_framework.views import APIView
from rest_framework.response import Response
from service.models.likes import Likes
from service.serializers.likes import LikesSerializer
import json

class PostLikesView(APIView):
    serializer_class = LikesSerializer
    
    def get(self, request, author, post):
        likes_query = Likes.objects.filter(object = post)
        likes = self.serializer_class(likes_query, many=True).data

        return Response({"likes": likes}, status=200)
        
class CommentLikesView(APIView):
    def get(self, request, author, post, comment):
        path = self.request.path_info

        likes_query = Likes.objects.filter(object = comment)
        likes = []
        for like in likes_query:
            likes.append(like.toJSON())

        return Response({"likes": likes})
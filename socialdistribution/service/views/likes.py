from rest_framework.views import APIView
from rest_framework.response import Response
from service.models.likes import Likes

class PostLikesView(APIView):
    def get(self, request, author, post):
        path = self.request.path_info

        Likes.objects.get(object = path[:-7])

        return Response({"author": author, "post": post})
        
class CommentLikesView(APIView):
    def get(self, request, author, post, comment):
        path = self.request.path_info

        Likes.objects.get(object = path[:-7])
        
        return Response({"author": author, "post": post, "comment": comment})
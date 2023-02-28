from rest_framework.views import APIView
from rest_framework.response import Response
from service.models.likes import Likes
from service.models.author import Author
from service.models.post import Post
from service.models.comment import Comment
from service.serializers.likes import LikesSerializer
import json

class LikesView(APIView):
    serializer_class = LikesSerializer

    def get(self, request, author, post, comment=None):
        if not Author.objects.filter(_id=author).exists():
            return Response({"error": "No author exists!"}, status=404)
        if not Post.objects.filter(_id=post).exists(): 
            return Response({"error": "No post exists!"}, status=404)        

        if not comment:
            likes_query = Likes.objects.filter(object = post)
        else:
            if Comment.objects.filter(_id=comment).exists():
                likes_query = Likes.objects.filter(object = comment)
            else:
                return Response({"error": "No comment exists!"}, status=404)


        likes = self.serializer_class(likes_query, many=True).data

        return Response({"likes": json.dumps(likes)}, status=200)
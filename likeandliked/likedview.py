from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Like
from .serializers import LikeSerializer

class LikedView(APIView):
    def get(self, request, author_id):
        likes = Like.objects.filter(author_id=author_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class LikesView(APIView):
    def get(self, request, author_id, post_id=None, comment_id=None):
        if post_id:
            likes = Like.objects.filter(post_id=post_id)
        elif comment_id:
            likes = Like.objects.filter(comment_id=comment_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, author_id, post_id=None, comment_id=None):
        data = request.data.copy()
        data['author_id'] = author_id
        if post_id:
            data['post_id'] = post_id
        elif comment_id:
            data['comment_id'] = comment_id
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

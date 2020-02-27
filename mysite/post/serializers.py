from rest_framework import serializers

from comment.serializer import CommentSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
        depth = 0

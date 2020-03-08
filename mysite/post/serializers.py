from rest_framework import serializers

from user.models import User
from user.serializers import AuthorSerializer
from comment.serializer import CommentSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = [
            "author",
        ]
        depth = 0

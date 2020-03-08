from rest_framework import serializers

from user.serializers import AuthorSerializer

# from post.serializers import PostSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return f"{obj.created_by.username}"

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "created_by",
            "content",
            "contentType",
            "published",
            "updated",
            "author",
        ]
        extra_kwargs = {"created_by": {"write_only": True}}


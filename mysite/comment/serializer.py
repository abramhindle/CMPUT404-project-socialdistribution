from rest_framework import serializers

# from user.serializers import AuthorSerializer
# from post.serializers import PostSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer(read_only=True)
    # post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "created_by",
            "content",
            "contentType",
            "published",
        ]
        read_only_fields = (
            "post",
            "created_by",
        )

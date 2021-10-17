from rest_framework import serializers
from .models import Comment, Like, Post
from author.serializers import AuthorCreationSerializer

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_id", read_only=True)
    type = serializers.CharField(default="comment", read_only=True)
    comment = serializers.CharField(source="get_content", read_only=True)
    published = serializers.DateTimeField(source="get_date", read_only=True)
    author = AuthorCreationSerializer(source="get_author")

    class Meta:
        model = Comment
        fields = ['id', 'type', 'comment', 'contentType', 'published', 'author']
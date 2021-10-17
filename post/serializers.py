from rest_framework import serializers
from .models import Comment, Like, Post
from author.models import Author
from author.serializers import AuthorSerializer
from datetime import datetime, timezone

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="get_id", read_only=True)
    type = serializers.CharField(default="comment", read_only=True)
    comment = serializers.CharField(source="get_content")
    published = serializers.DateTimeField(source="get_date", read_only=True)
    author = AuthorSerializer(source="get_author")

    class Meta:
        model = Comment
        fields = ['id', 'type', 'comment', 'contentType', 'published', 'author']

    def create(self, validated_data):
        post_id = self.context["post_id"]
        author_id = self.context["author_id"]
        post = Post.objects.get(postID=post_id)
        author = Author.objects.get(authorID=author_id)
        date = datetime.now(timezone.utc).astimezone().isoformat()
        print(validated_data)
        content = validated_data["get_content"]
        contentType = validated_data["contentType"]
        return Comment.objects.create(postID=post, authorID=author, date=date, content=content, contentType=contentType)
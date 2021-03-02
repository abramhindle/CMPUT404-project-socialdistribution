from rest_framework import serializers
from presentation.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['_type', 'author', 'post', 'comment', 'contentType', 'published', 'id']

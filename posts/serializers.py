from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Post, Comment
from authors.serializers import AuthorSerializer

class PostSerializer(serializers.ModelSerializer):
    # type is only provided to satisfy API format
    type = serializers.CharField(default="post", source="get_api_type", read_only=True)
    # public id should be the full url
    id = serializers.CharField(source="get_public_id", read_only=True)
    count = serializers.IntegerField(source="count_comments", read_only=True)
    published = serializers.DateTimeField(read_only=True)
    author = AuthorSerializer(read_only=True)

    # e.g. 'PUBLIC'
    visibility = serializers.ChoiceField(choices=Post.Visibility.choices)
    # e.g. 'text/markdown'
    contentType = serializers.ChoiceField(choices=Post.ContentType.choices, source='content_type')

    # TODO: missing the following fields
    # categories, size, comments (url), comments (Array of JSON)
    class Meta:
        model = Post
        # show these fields in response
        fields = [
            'type', 
            'id', 
            'title', 
            'source', 
            'origin', 
            'description',
            'contentType',
            'author',
            'content',
            'count',
            'published',
            'visibility',
            'unlisted'
        ]

class CommentSerializer(serializers.ModelSerializer):
    # type is only provided to satisfy API format
    type = serializers.CharField(default="comment", source="get_api_type", read_only=True)
    # public id should be the full url
    id = serializers.CharField(source="get_public_id", read_only=True)
    
    #TODO: is the the author who commented or the post's author?
    author = AuthorSerializer(read_only=True)
    contentType = serializers.ChoiceField(choices=Post.ContentType.choices, source='content_type')

    class Meta:
        model = Comment
        fields = [
            "type",
            "author",
            "comment",
            "contentType",
            "published",
            "id"
        ]
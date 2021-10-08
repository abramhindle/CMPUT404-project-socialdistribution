from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Post
from authors.serializers import AuthorSerializer

class PostSerializer(serializers.ModelSerializer):
    # type is only provided to satisfy API format
    type = serializers.CharField(default="post", source="get_api_type", read_only=True)
    # public id should be the full url
    id = serializers.CharField(source="get_public_id", read_only=True)
    count = serializers.IntegerField(source="count_comments", read_only=True)
    visibility = serializers.CharField(source="get_visilibility_label")
    published = serializers.DateTimeField(read_only=True)
    contentType = serializers.CharField(source='get_content_type_label')
    author = AuthorSerializer(read_only=True)

    # TODO: missing the following fields
    # categories, size, comments (url), comments (Array of JSON)

    # validate and return the label of the visibility
    def validate_visibility(self, visibility):
        try: 
            visibility = Post.Visibility(visibility).label
            return visibility
        except ValueError as error:
            raise serializers.ValidationError(f"{error} is not a valid visibility")

    # validate and return the label of the content type
    def validate_contentType(self, content_type):
        try: 
            content_type = Post.ContentType(content_type).label
            return content_type
        except ValueError as error:
            raise serializers.ValidationError(f"{error} is not a valid content type")

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


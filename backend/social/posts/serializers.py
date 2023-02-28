from rest_framework import serializers
from .models import Post

PUBLIC = 'PUBLIC'
PRIVATE = 'PRIVATE'
FRIENDS = 'FRIENDS'

visbility_choices = [
    (PUBLIC, 'PUBLIC'),
    (PRIVATE, 'PRIVATE'),
    (FRIENDS, 'FRIENDS')
]

MARKDOWN = 'text/markdown'
PLAIN = 'text/plain'
IMAGE_PNG = 'image/png'
IMAGE_JPEG = 'image/jpeg'

content_types = [
    (MARKDOWN, 'markdown'),
    (PLAIN, 'plain'),
    (IMAGE_PNG, 'image/png;base64'),
    (IMAGE_JPEG, 'image/jpeg;base64'),
]

class PostSerializer(serializers.Serializer):
    type = serializers.CharField(default="post",source="get_api_type",read_only=True)
    title = serializers.CharField(max_length=150)  # title of post
    source = serializers.URLField(default="",max_length=500)  # source of post
    origin = serializers.URLField(default="",max_length=500)  # origin of post
    description = serializers.CharField(blank=True, default="", max_length=200)  # brief description of post
    content_type = serializers.CharField(choices=content_types, default=PLAIN, max_length=20)  # type of content
    content = serializers.TextField(blank=False, default="")  # content of post
    visibility = serializers.CharField(choices=visbility_choices, default=PUBLIC, max_length=20)  # visibility status of post

    def create(self, validated_data):
        """
        Create and return a new `Post` instance, given the validated data
        """
        return Post.object.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Post` instance, given the validated data
        """
        instance.title = validated_data.get('title', instance.title)
        instance.source = validated_data.get('source', instance.pub_date)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.description = validated_data.get('description', instance.description)
        instance.content_type = validated_data.get('content_type', instance.content_type)
        instance.content = validated_data.get('content', instance.content)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.save()
        return instance
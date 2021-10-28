# Implementation of serializers from the tutorial: https://www.django-rest-framework.org/tutorial/1-serialization/

from rest_framework import serializers
from apps.core.serializers import UserSerializer
from apps.posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="post", read_only=True)
    id = serializers.CharField(source="get_post_id", read_only=True)
    contentType = serializers.ChoiceField(choices=Post.ContentTypeEnum.choices, default=Post.ContentTypeEnum.PLAIN)
    author = UserSerializer(read_only=True)
    visibility = serializers.ChoiceField(choices=Post.VisibilityEnum.choices, default=Post.VisibilityEnum.PUBLIC)


    class Meta:
        model = Post
        fields = [
            'type', 
            'title', 
            'id', 
            # 'source',
            # 'origin',
            'description',
            'contentType',
            'author',
            # 'categories',
            # 'count',
            # 'comments',
            'published',
            'visibility',
            'unlisted'
        ]
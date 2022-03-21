from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from posts.models import Post


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'url', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = 'author'
        representation['displayName'] = instance.get_full_name()
        representation['github'] = instance.github_url
        representation['profileImage'] = instance.profile_image_url
        return representation


class PostSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'author_pk': 'author__pk',
    }
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'author', 'visibility', 'unlisted', 'url']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = 'post'
        representation['contentType'] = instance.content_type
        representation['published'] = instance.date_published
        representation['categories'] = [category.category for category in instance.categories.all()]
        return representation

from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Author, InboxObject

class AuthorSerializer(serializers.ModelSerializer):
    # type is only provided to satisfy API format
    type = serializers.CharField(default="author", read_only=True)
    # public id should be the full url
    id = serializers.CharField(source="get_public_id", read_only=True)
    displayName = serializers.CharField(source='display_name')
    github = serializers.CharField(source='github_url')

    """
    method used to modify model, if serializer is used as `partial=True`
    """
    def update(self, instance, validated_data):
        instance.github_url = validated_data.get('github_url', instance.github_url)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.save()
        return instance

    """
    validator that will run on `github` field on .is_valid() call
    """
    def validate_github(self, value):
        if value and not 'github.com' in value:
            raise ValidationError(_('Author github url has to be a github url.'))
        return value

    class Meta:
        model = Author
        # show these fields in response
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github']

class FriendRequestSerializer(serializers.Serializer):
    """
    used to parse incoming POST /inbox/ where the json object is a FriendRequest,
    sent from another server.

    It expects the author object to conform to our AuthorSerializer.
    """
    type = serializers.HiddenField(default='Follow')
    summary = serializers.CharField()
    actor = AuthorSerializer()
    object = AuthorSerializer()


class InboxObjectSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    object = serializers.JSONField()
    class Meta:
        model = InboxObject
        fields = ['author', 'object']

    def to_internal_value(self, data):
        # author is only used internally
        author = self.context.get('author')
        validated_data = {
            'author': author,
            'object': data
        }
        return validated_data

    def to_representation(self, instance):
        # the representation/external output is just the json object
        return instance.object

    def create(self, validated_data):
        return InboxObject.objects.create(**validated_data)

import uuid
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from rest_framework import exceptions, serializers

from .models import Author, FriendRequest, InboxObject


class AuthorSerializer(serializers.ModelSerializer):
    # type is only provided to satisfy API format
    type = serializers.CharField(default="author", read_only=True)
    # public id should be the full url
    id = serializers.CharField()
    displayName = serializers.CharField(source='display_name', required=False, allow_null=True)
    github = serializers.CharField(source='github_url', required=False, allow_null=True)
    url = serializers.URLField(required=False)
    host = serializers.URLField(required=False)

    def to_representation(self, instance):
        return {
            **super().to_representation(instance),
            'id': instance.get_public_id()
        }

    def update(self, instance, validated_data):
        """
        method used to modify model, if serializer is used as `partial=True`
        """
        instance.github_url = validated_data.get(
            'github_url', instance.github_url)
        instance.display_name = validated_data.get(
            'display_name', instance.display_name)
        instance.save()
        return instance

    def create(self, validated_data):
        # allow partial update as .save()
        author, created = Author.objects.update_or_create(**validated_data)
        return author

    def upcreate_from_validated_data(self):
        if not self.is_valid():
            raise exceptions.ParseError("data not valid")
        try:
            updated_author = self.update(Author.objects.get(
                id=self.validated_data['id']), self.validated_data)
        except:
            updated_author = Author.objects.create(
                **self.validated_data)
        return updated_author

    def validate_github(self, value):
        """
        validator that will run on `github` field on .is_valid() call
        """
        if value and not 'github.com' in value:
            raise ValidationError(
                _('Author github url has to be a github url.'))
        return value

    class Meta:
        model = Author
        # show these fields in response
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github']


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    used to parse incoming POST /inbox/ where the json object is a FriendRequest,
    sent from another server.

    It expects the author object to conform to our AuthorSerializer.
    """
    type = serializers.CharField(default='Follow', read_only=True)
    summary = serializers.CharField()
    actor = AuthorSerializer()
    object = AuthorSerializer()

    def create(self, validated_data):
        actor, created = Author.objects.update_or_create(**validated_data['actor'])
        object = Author.objects.get(url=validated_data['object']['url'])
        return FriendRequest.objects.create(summary=validated_data['summary'], actor=actor, object=object)

    def validate_object(self, data):
        serializer = AuthorSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            raise exceptions.ParseError

        try:
            Author.objects.get(Q(id=serializer.validated_data.get('id')) | Q(url=serializer.validated_data.get('url')))
        except:
            # the object author does not exist. we cannot create a new author out of nothing
            raise exceptions.ParseError
        return serializer.validated_data

    class Meta:
        model = FriendRequest
        fields = ['summary', 'actor', 'object', 'type']


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

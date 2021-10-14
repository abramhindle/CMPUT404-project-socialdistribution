from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    # type is only provided to satisfy API format
    type = serializers.HiddenField(default="author")
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
        if value and not value.startswith('https://github.com'):
            raise ValidationError(_('Author github url has to be a github url.'))
        return value

    class Meta:
        model = Author
        # show these fields in response
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github']

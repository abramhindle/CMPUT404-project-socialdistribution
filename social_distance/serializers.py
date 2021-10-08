from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from authors.models import Author

from authors.serializers import AuthorSerializer


class CommonAuthenticateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    author = AuthorSerializer(read_only=True)

    def to_representation(self, instance):
        """
        final customization to make for the output object:
        - add tokens to the reponse body
        """
        base_dict = {
            'username': instance.username,
            'author': AuthorSerializer(instance.author).data if hasattr(instance, 'author') else None
        }
        refresh = RefreshToken.for_user(instance)
        access = refresh.access_token

        base_dict['access_token'] = str(access)
        base_dict['refresh_token'] = str(refresh)

        return base_dict


class RegisterSerializer(CommonAuthenticateSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    display_name = serializers.CharField(required=False)
    github_url = serializers.URLField(required=False)

    def create(self, validated_data):
        """
        called when calling .save(), create objects from validated_data
        """
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        author = Author(user=user, display_name=validated_data.get(
            'display_name', user.username), github_url=validated_data.get('github_url'))
        # modify url to be server path
        author.update_fields_with_request(self.context['request'])
        author.save()
        return user

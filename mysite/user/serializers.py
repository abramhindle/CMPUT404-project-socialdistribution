from rest_framework import serializers, exceptions
from rest_framework.pagination import PageNumberPagination
from rest_auth.serializers import LoginSerializer
from django.utils.translation import ugettext_lazy as _

from .models import User


class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = None
        # Authentication through email
        user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_approve:
                msg = _("Please wait the admin to approve your register request")
                raise exceptions.ValidationError(msg)
        else:
            if not User.objects.filter(email=email).exists():
                msg = _("This email has not registered yet.")
            else:
                msg = _("The email and the password are not matched.")
            raise exceptions.ValidationError(msg)

        attrs["user"] = user
        return attrs


class AuthorSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        return f"{obj.host}author/{obj.username}"

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "displayName",
            "host",
            "github",
            "bio",
            "url",
        ]
